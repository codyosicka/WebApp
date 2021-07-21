from website import create_app

app = create_app()

if __name__ == '__main__': # only if we run this file (not import it), we are going to execute the following lines 
	app.run(debug=True)

	