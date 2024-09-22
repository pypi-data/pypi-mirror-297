from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from killbill_xml_builder.builders.products import Product
from killbill_xml_builder.builders.plans import Plan


def get_effective_date():
    """Return the current date and time in UTC"""

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def add_product(catalog: str, product: Product):
    """Add product to catalog"""

    root = ET.fromstring(catalog)
    effective_date_element = root.find("effectiveDate")
    effective_date_element.text = get_effective_date()

    products_element = root.find("products")
    products_element.append(product.element)

    return ET.tostring(root, encoding="unicode")


def add_plan(catalog: str, plan: Plan):
    """Add plan to catalog"""

    root = ET.fromstring(catalog)
    effective_date_element = root.find("effectiveDate")
    effective_date_element.text = get_effective_date()

    plans_element = root.find("plans")
    plans_element.append(plan.element)

    price_list_element = root.find("priceLists").find("defaultPriceList").find("plans")
    plan_element = ET.SubElement(price_list_element, "plan")
    plan_element.text = plan.name

    return ET.tostring(root, encoding="unicode")
