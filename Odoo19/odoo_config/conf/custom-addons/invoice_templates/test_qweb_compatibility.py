#!/usr/bin/env python3
"""
QWeb Compatibility Test for Invoice Templates

This script checks for common QWeb compatibility issues that can cause
template compilation errors in Odoo.
"""

import os
import sys
import re
import xml.etree.ElementTree as ET

def check_td_field_usage(file_path):
    """Check for t-field usage directly on td elements"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse XML to check structure
        root = ET.fromstring(content)
        
        # Find all td elements with t-field attribute
        for td in root.iter('td'):
            if 't-field' in td.attrib:
                line_num = "unknown"  # ET doesn't provide line numbers easily
                issues.append(f"td element with t-field attribute found (line {line_num})")
        
        # Also check with regex for more detailed line info
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(r'<td[^>]*t-field[^>]*>', line):
                issues.append(f"Line {i}: td element with t-field attribute")
        
        return issues
        
    except Exception as e:
        return [f"Error parsing file: {str(e)}"]

def check_table_field_usage(file_path):
    """Check for t-field usage on other problematic table elements"""
    problematic_elements = ['table', 'tbody', 'thead', 'tfoot', 'tr', 'th']
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            for element in problematic_elements:
                pattern = f'<{element}[^>]*t-field[^>]*>'
                if re.search(pattern, line):
                    issues.append(f"Line {i}: {element} element with t-field attribute")
        
        return issues
        
    except Exception as e:
        return [f"Error checking table elements: {str(e)}"]

def check_xml_entities(file_path):
    """Check for unescaped XML entities"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for unescaped ampersands (but not already escaped ones)
            if re.search(r'&(?!amp;|lt;|gt;|quot;|apos;)', line):
                issues.append(f"Line {i}: Unescaped ampersand found")
            
            # Check for unescaped < and > in attribute values
            if re.search(r'="[^"]*<[^"]*"', line) or re.search(r'="[^"]*>[^"]*"', line):
                issues.append(f"Line {i}: Unescaped < or > in attribute value")
        
        return issues
        
    except Exception as e:
        return [f"Error checking XML entities: {str(e)}"]

def test_template_file(file_path):
    """Test a single template file for QWeb compatibility"""
    print(f"Testing: {file_path}")
    
    all_issues = []
    
    # Test for td t-field issues
    td_issues = check_td_field_usage(file_path)
    if td_issues:
        all_issues.extend([f"  TD t-field: {issue}" for issue in td_issues])
    
    # Test for other table element issues
    table_issues = check_table_field_usage(file_path)
    if table_issues:
        all_issues.extend([f"  Table t-field: {issue}" for issue in table_issues])
    
    # Test for XML entity issues
    entity_issues = check_xml_entities(file_path)
    if entity_issues:
        all_issues.extend([f"  XML Entity: {issue}" for issue in entity_issues])
    
    if all_issues:
        print("  ❌ Issues found:")
        for issue in all_issues:
            print(f"    {issue}")
        return False
    else:
        print("  ✅ No QWeb compatibility issues found")
        return True

def main():
    """Main test function"""
    print("🧪 QWeb Compatibility Test for Invoice Templates\n")
    
    # Find all template files
    template_files = []
    if os.path.exists('report'):
        for file in os.listdir('report'):
            if file.endswith('.xml') and 'template' in file:
                template_files.append(os.path.join('report', file))
    
    if not template_files:
        print("❌ No template files found")
        return False
    
    print(f"Found {len(template_files)} template files to test:\n")
    
    passed = 0
    total = len(template_files)
    
    for template_file in template_files:
        if test_template_file(template_file):
            passed += 1
        print()
    
    print(f"📊 QWeb Compatibility Results:")
    print(f"  Compatible templates: {passed}/{total}")
    print(f"  Templates with issues: {total - passed}")
    
    if passed == total:
        print(f"\n🎉 All templates are QWeb compatible!")
        print(f"\n💡 Common QWeb Rules:")
        print(f"  - Don't use t-field directly on table elements (td, tr, table, etc.)")
        print(f"  - Wrap t-field in span or div elements inside table cells")
        print(f"  - Escape XML entities: & → &amp;, < → &lt;, > → &gt;")
        print(f"  - Use proper XML structure with closed tags")
        return True
    else:
        print(f"\n❌ Some templates have QWeb compatibility issues.")
        print(f"\n🔧 Common Fixes:")
        print(f"  - Replace <td t-field='...'> with <td><span t-field='...'/></td>")
        print(f"  - Replace & with &amp; in XML content")
        print(f"  - Ensure all XML tags are properly closed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
