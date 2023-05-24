
from flask import abort, render_template
from flask_login import current_user, login_required
from ..models import Customer,Product
from . import customers


@customers.route('/products',methods=['GET','POST'])
@login_required
def view_products():
    """Customer view products"""

    products = Product.query.all()
    print(f'Products: {products}')
    image_urls = {}
    for product in products:
        if product.image_path:
            image_urls[product.id] = f'/static/img/{product.image_path}'

    print(image_urls)
    return render_template('customer/customer_products.html',
                           products=products, title="Products",image_urls=image_urls,Customer=Customer)