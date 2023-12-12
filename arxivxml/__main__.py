import pandas as pd
from lxml import etree
from datetime import datetime
import argparse
import toml

def publicationReference(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = toml.load(config_file)
            pub_ref = config.get('pub_ref', '')
        return pub_ref
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        return None

def generate_xml_from_ods(file_path, config_path):
    # Read .ods file
    df = pd.read_excel(file_path, engine='odf')

    # Extract unique affiliations
    affiliations = set(df.iloc[:, 5:8].fillna('').values.flatten()) - {''}

    # XML root
    root = etree.Element("collaborationauthorlist", nsmap={
        'foaf': "http://xmlns.com/foaf/0.1/",
        'cal': "http://inspirehep.net/info/HepNames/tools/authors_xml/"
    })

    # Creation date
    creation_date = etree.SubElement(root, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}creationDate")
    creation_date.text = datetime.now().strftime("%Y-%m-%d")

    # Publication reference
    pub_ref = etree.SubElement(root, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}publicationReference")
    pub_ref.text = publicationReference(config_path)

    # Organizations
    organizations = etree.SubElement(root, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}organizations")
    for idx, aff in enumerate(sorted(affiliations), 1):
        org = etree.SubElement(organizations, "{http://xmlns.com/foaf/0.1/}Organization", id=f"a{idx}")
        etree.SubElement(org, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}orgDomain").text = "http://"
        etree.SubElement(org, "{http://xmlns.com/foaf/0.1/}name").text = aff
        etree.SubElement(org, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}orgStatus", collaborationid="c1")

    # Authors
    authors = etree.SubElement(root, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}authors")
    for _, row in df.iterrows():
        person = etree.SubElement(authors, "{http://xmlns.com/foaf/0.1/}Person")
        etree.SubElement(person, "{http://xmlns.com/foaf/0.1/}givenName").text = row[0]  # First name
        etree.SubElement(person, "{http://xmlns.com/foaf/0.1/}familyName").text = row[2]  # Last name
        # ORCID if available
        if pd.notna(row[4]):
            author_ids = etree.SubElement(person, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}authorids")
            author_id = etree.SubElement(author_ids, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}authorid", source="ORCID")
            author_id.text = row[4]
        # Affiliations
        author_affiliations = etree.SubElement(person, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}authorAffiliations")
        for aff in row[5:8].dropna():
            idx = sorted(affiliations).index(aff) + 1
            etree.SubElement(author_affiliations, "{http://inspirehep.net/info/HepNames/tools/authors_xml/}authorAffiliation", organizationid=f"a{idx}")

    # Return XML string
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Generate XML from ODS file containing author list.")
    parser.add_argument("file_path", type=str, help="Path to the .ods file containing the author list")
    parser.add_argument("--toml", type=str, help="Path to the toml file containing the publication reference")


    # Parse arguments
    args = parser.parse_args()

    # Generate XML content from .ods file
    xml_content = generate_xml_from_ods(args.file_path, args.toml)

    # Output the XML content
    with open("authors.xml", "w", encoding="UTF-8") as file:
        file.write(xml_content)

if __name__ == "__main__":
    main()