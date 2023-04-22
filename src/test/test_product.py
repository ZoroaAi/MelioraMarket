# tests/test_product.py

from flask import request
from flask_paginate import Pagination
from flask_testing import TestCase
from src import create_app
from src.models import Product, db
from bs4 import BeautifulSoup


class TestProduct(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        test_product1 = Product(title="Test Product 1", price=10, market_name="Tesco", img_url="https://example.com/example_image1")
        test_product2 = Product(title="Test Product 2", price=5, market_name="Morrisons", img_url="https://example.com/example_image1")
        db.session.add(test_product1)
        db.session.add(test_product2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_filtered_browse_price_sort(self):
        # Test ascending price sort
        product1 = Product(title='Test Product 1', price=5.0, market_name='Test Market', img_url="https://example.com/example_image1")
        product2 = Product(title='Test Product 2', price=3.0, market_name='Test Market', img_url="https://example.com/example_image2")
        product3 = Product(title='Test Product 3', price=7.0, market_name='Test Market', img_url="https://example.com/example_image3")
        db.session.add_all([product1, product2, product3])
        db.session.commit()

        response_asc = self.client.get('/filtered-browse?price_order=asc')
        self.assertEqual(response_asc.status_code, 200)

        # Write the response content to a file for debugging
        with open('response.html', 'wb') as f:
            f.write(response_asc.data)

        # Check if the product card for "Test Product 2" is present
        card_title = response_asc.html.find(text='Test Product 2')
        card_price = response_asc.html.find(text='\xa33.00')
        card_market = response_asc.html.find(text='Test Market')
        card_image = response_asc.html.find('img', attrs={'src': 'https://example.com/example_image2'})

        product2_card_found = all([card_title, card_price, card_market, card_image])
        self.assertTrue(product2_card_found, f"Product card for 'Test Product 2' not found. Title: {card_title}, Price: {card_price}, Market: {card_market}, Image: {card_image}")
