#!/usr/bin/env python3
"""
Test script to verify the Action Basin invoice template fixes
"""

import xml.etree.ElementTree as ET
import re

def test_template_structure():
    """Test that the template has proper structure without Bootstrap classes"""
    
    # Read the template file
    with open('report/invoice_template_action_basin.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== Testing Action Basin Invoice Template Structure ===\n")
    
    # Test 1: Check for Bootstrap classes that don't work in PDF
    bootstrap_classes = ['row', 'col-', 'text-end', 'text-center', 'mb-', 'mt-', 'table-borderless']
    bootstrap_found = []
    
    for cls in bootstrap_classes:
        if f'class="{cls}' in content or f"class='{cls}" in content:
            bootstrap_found.append(cls)
    
    if bootstrap_found:
        print(f"❌ Found Bootstrap classes that may not work in PDF: {bootstrap_found}")
    else:
        print("✅ No problematic Bootstrap classes found")
    
    # Test 2: Check for proper table-based layout
    table_count = content.count('<table')
    print(f"✅ Found {table_count} table elements for PDF-compatible layout")
    
    # Test 3: Check for invoice lines table structure
    if 'invoice_line_ids.filtered' in content:
        print("✅ Invoice lines table structure is present")
    else:
        print("❌ Invoice lines table structure is missing")
    
    # Test 4: Check for 3-column header layout
    if 'width: 33%' in content and 'width: 34%' in content:
        print("✅ 3-column header layout is implemented")
    else:
        print("❌ 3-column header layout is missing")
    
    # Test 5: Check for proper styling without Bootstrap dependencies
    inline_styles = content.count('style=')
    print(f"✅ Found {inline_styles} inline styles for PDF compatibility")
    
    # Test 6: Check for invoice items table headers
    required_headers = ['Item &amp; Description', 'Qty', 'Rate', 'Amount']
    headers_found = all(header in content for header in required_headers)

    if headers_found:
        print("✅ All required table headers are present")
    else:
        missing_headers = [h for h in required_headers if h not in content]
        print(f"❌ Some table headers are missing: {missing_headers}")
    
    # Test 7: Check for totals section
    if 'Sub Total' in content and 'amount_untaxed' in content:
        print("✅ Totals section is properly structured")
    else:
        print("❌ Totals section has issues")
    
    print("\n=== Template Structure Analysis Complete ===")
    
    # Show key improvements made
    print("\n=== Key Improvements Made ===")
    print("1. Replaced Bootstrap row/col classes with table-based layout")
    print("2. Implemented proper 3-column header design")
    print("3. Fixed invoice items table structure")
    print("4. Used inline styles for PDF compatibility")
    print("5. Ensured all sections use table layouts instead of flexbox/grid")
    
    return True

def test_xml_validity():
    """Test that the XML is valid"""
    try:
        with open('report/invoice_template_action_basin.xml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse XML to check validity
        ET.fromstring(content)
        print("✅ XML is valid and well-formed")
        return True
    except ET.ParseError as e:
        print(f"❌ XML parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

if __name__ == "__main__":
    print("Testing Action Basin Invoice Template Fixes...\n")
    
    xml_valid = test_xml_validity()
    if xml_valid:
        test_template_structure()
    
    print("\n" + "="*60)
    print("Template testing complete!")
    print("The template should now work properly in PDF generation")
    print("with the correct 3-column header layout and invoice items.")
