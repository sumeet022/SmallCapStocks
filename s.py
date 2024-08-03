import pandas as pd
import xml.etree.ElementTree as ET

# Sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)

# Convert DataFrame to XML
root = ET.Element('data')
for index, row in df.iterrows():
    person = ET.SubElement(root, 'person')
    for col_name, col_value in row.iteritems():
        print(col_name,col_value)
        ET.SubElement(person, col_name).text = str(col_value)

tree = ET.ElementTree(root)
# tree.write('output.xml', encoding='utf-8', xml_declaration=True)
