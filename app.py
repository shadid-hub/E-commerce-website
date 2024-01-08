from flask import Flask, render_template , request
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length , Regexp



app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bean_factory.db'
app.secret_key = 'bean_bois'
db = SQLAlchemy(app)

class Bean(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Float,nullable=False)
    CF = db.Column(db.Float,nullable=False)
    img_src = db.Column(db.String(256),nullable=False)
    description = db.Column(db.String(256),nullable=False)


@app.route('/')
def home():
    sort_by = request.args.get('sort_by', default='id')
    order = request.args.get('order' , default='asc')

    if hasattr(Bean, sort_by):
       column_to_sort = getattr(Bean, sort_by)
       if order== 'asc':
        beans = Bean.query.order_by(column_to_sort.asc()).all()
       else:
        beans = Bean.query.order_by(column_to_sort.desc()).all()
    else:
      beans = Bean.query.order_by(Bean.name.asc()).all()
    beans_in_cart = len(session.get("scart",[]))
    return render_template('index.html', beans=beans)

@app.route('/bean/<int:bean_id>')
def bean(bean_id):
 bean = Bean.query.get(bean_id)
 return render_template('beandesc.html', bean=bean)

@app.route('/add_to_scart/<int:id>')
def add_to_scart(id):
  if "scart" not in session:
    session["scart"] = []

  session["scart"].append(id)
  session.modified = True
  return redirect(request.referrer)

@app.route('/scart')
def scart():
  scart_beans = []
  total_price = 0

  for id in session.get("scart", []):
    bean = Bean.query.get(id)
    if bean:
      scart_beans.append(bean)
      total_price += bean.price
  bean_in_cart = len(session.get("scart",[]))
  return render_template('scart.html', scart_beans=scart_beans, total_price=total_price)
  
@app.route('/remove_from_scart/<int:id>')
def remove_from_scart(id):
     if "scart" in session and id in session["scart"]:
       session["scart"].remove(id)
       session.modified = True
     return redirect(url_for('scart'))
     
@app.route('/clear_scart')
def clear_scart():
    session.pop("scart", None)
    return redirect(url_for('scart'))
  

class PaymentForm(FlaskForm):
  card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=19), Regexp('^[0-9 -]*$' , message="Not Valid Card Number")], render_kw={"title": "Enter 16 Digit Card Number Please"})
  name_on_card = StringField('Name on Card', validators=[DataRequired()], render_kw={"title": "Enter Name"})
  expiry_date = StringField('Expiry Date', validators=[DataRequired(), Length(min=3, max=4), Regexp('^[0-9]*$', message="Only Numerical year")], render_kw={"title": "Enter the Expiry date"})
  cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3), Regexp('^[0-9]*$', message="Only Numbers")], render_kw={"title": "Last 3 digits on the back of your card"})
  submit = SubmitField('Submit Payment')

@app.route('/checkout', methods=['get', 'POST'])
def checkout():
  form = PaymentForm()
  if form.validate_on_submit():
    return render_template('approved.html')
  return render_template('checkout.html' , form=form)
  


if __name__ == '__main__':
 with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(Bean(name='Blue Beans', price=2, CF=12, description='Great Blue Beans , All the way from Brazil , Super flavour, quite spicy. Can use for curries, or other dishes. ', img_src='/static/img/DALL·E 2023-05-07 06.44.44 - blue beans.png'))
    db.session.add(Bean(name='Special bundle', price=4, CF=14, description='A great offer , only last till the end of the year. Get a bundle of multiple beans , each with its own amaizing flavour, spicy, sweet and sour',img_src='/static/img/bundle.PNG'))
    db.session.add(Bean(name='Dried Beans', price=5, CF=15, description='good Old , dried beans, great for some sauces or for some other dishes, can be eaten directly.',img_src='/static/img/dired beans.png'))
    db.session.add(Bean(name='Red Beans', price=6, CF=18, description='Your day to day red beans, spicy and sweet in flavour. Can be eaten directly or used for curries and rice. Please Wash before use',img_src='/static/img/close-up-red-beans-background-15940478546g2.jpg'))
    db.session.add(Bean(name='Rocky Beans', price=7, CF=20, description='Hard rocky beans, unless you want to break your teeth, do not eat them directly, they get their names for a reaason!. used best for adding flavour to ready made dishes',img_src='/static/img/R.jpg'))
    db.session.add(Bean(name='Baked beans', price=8, CF=25, description='Plain baked beans, best for people who do not have the time for prepping meals, scoop up and just eat. Covered in marinated sauces. YUM',img_src='/static/img/oven-baked-pinto-beans_0.jpg'))
    db.session.add(Bean(name='Cofee', price=9, CF=26, description='Coffe beans, great for brewing coffee, they come all the way from ghana, rich in flavour, will not dissapoint.',img_src='/static/img/OIP.jpg'))
    db.session.add(Bean(name='Dried Beans', price=10,CF=30, description='These beans are dried to lock in their flavor and nutrients, making them a staple in many cuisines.',img_src='/static/img\king beans 2.jpg'))
    db.session.add(Bean(name='Curry Beans', price=11,CF=50, description='Bursting with flavor, these beans are perfect for creating hearty and warming curries',img_src='/static/img/images.jpg'))
    db.session.add(Bean(name='Clarity Beans',price=100,CF=55, description='These beans are known for their distinctive clear skin, adding a unique touch to any dish.',img_src='/static/img/DALL·E 2023-05-07 06.49.35 - neon beans.png'))
    db.session.add(Bean(name='Brown Beans',price=13,CF=60, description='With their subtle, earthy flavor, brown beans are a versatile addition to any recipe',img_src='/static/img/DALL·E 2023-05-07 06.47.43 - brown beans.png'))
    db.session.add(Bean(name='Multicoloured Beans',price=16,CF=62, description='A vibrant mixture of beans that not only looks good but also provides a variety of flavors.',img_src='/static/img/DALL·E 2023-05-07 06.50.12 - multicoloured.png'))
    db.session.add(Bean(name='Orange Beans',price=17,CF=65, description='With a unique citrus twist, these beans bring a burst of color and flavor to any dish.',img_src='/static/img/DALL·E 2023-05-07 06.58.58 - dark orange beans.png'))
    db.session.add(Bean(name='Rough Beans',price=18,CF=70, description='These beans have a rough exterior but inside they offer a rich, dense flavor.',img_src='/static/img/rough beans.png'))
    db.session.add(Bean(name='Indian Beans',price=19,CF=75, description='These beans, often used in Indian cooking, are known for their strong flavor and satisfying texture',img_src='/static/img/indian beans.png'))
    db.session.commit()
    app.run(debug=True)



