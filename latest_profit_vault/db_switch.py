from engineroom import app,db
wish=input("enter 0 if you want to delete and 1 if you want to create	:")
wish = int(wish)
if wish == 0:
	with app.app_context():
		db.drop_all()
	print("✅ All tables dropped.")
	
else:
	with app.app_context():
		db.create_all()
	print("✅ All tables created.")