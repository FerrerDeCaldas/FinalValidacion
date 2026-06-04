def load_login_context():
	return {
		"session_status": "success",
		"message": "You logged into a secure area!",
		"user": "test_user",
	}


def load_manufacturing_context():
	return {
		"module": "Manufacturing",
		"process": "BOM creation",
		"status": "ready",
	}


def load_quality_management_context():
	return {
		"module": "Quality Management",
		"process": "quality review",
		"status": "approved",
	}


def load_shopping_cart_context():
	return {
		"module": "Shopping Cart",
		"cart_total": 125.50,
		"discounts": ["seasonal", "bulk"],
	}
