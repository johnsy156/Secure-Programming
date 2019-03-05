import mysql.connector
import sys
import re

def main():

	oper = sys.argv[1]
	if oper == "ADD":
		if len(sys.argv) < 4:
			print("You have not specified enough arguments as input. Please provide input in the following format for the operation:")
			print("ADD --> ADD <NAME> <PHONENUMBER>")
		else:
			print("Operation to be performed", sys.argv[1])
			oper = sys.argv[1]
			name = sys.argv[2]
			phone = sys.argv[3]
			ADD(name,phone)
		
	elif oper == "LIST":
		print("Operation to be performed", sys.argv[1])
		LIST()
		
	elif oper == "DEL":
		if len(sys.argv) < 3:
			print("You have not specified enough arguments as input. Please provide input in the following format for the desired operation:")
			print("DEL --> DEL <name> or DEL <phone number>")
		
		else:
			print("Operation to be performed", sys.argv[1])
			value = sys.argv[2]	
			DEL(value)		
			

def ADD(name,phone):
	Conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'system', db = 'pysecure', port='3306')
	matchname = re.match("^([a-zA-Z][']?[a-zA-Z]*\\s*[\,]?\\s*?[a-zA-Z][']?[a-zA-Z]*[\-]*[a-zA-Z]?\\s*?[a-zA-Z]*\\.*)$",name)
	matchno = re.match("^(([\+]\d{1,2})?(\s?[\(]\d{1,2}[\)]\s?)?((\d{1})?[\(]\d{1,3}[\)])?(\d{3}[-]\d{4})?((\d{1,3}\s)+\d{4})*(\d{5,9})?(\d{5}[.]\d{5})?)$", phone)

	if matchname and matchno:
		print("Valid input")
		try:
			curConn = Conn.cursor()
			curConn.execute("""INSERT INTO secprj(name,phonenumber) values(%s, %s)""",(name,phone))
			Conn.commit()
	
		finally:
			Conn.close()
		sys.stderr.write("The values were inserted in the table")
		sys.exit(0)
	else:
		sys.stderr.write("Invalid input. Please try again")
		sys.exit(1)

	
def LIST():

	Conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'system', db = 'pysecure', port='3306')
	
	try:
		curConn = Conn.cursor()
		print("List all the values in the table")
		curConn.execute("""select * from secprj""")	
		finalres = curConn.fetchall()
		print(finalres)
	
	finally:
		Conn.close()
		
def DEL(value):
	
	Conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'system', db = 'pysecure', port='3306')
	matchname = re.match("^([a-zA-Z][']?[a-zA-Z]*\\s*[\,]?\\s*?[a-zA-Z][']?[a-zA-Z]*[\-]*[a-zA-Z]?\\s*?[a-zA-Z]*\\.*)$",value)
	matchno = re.match("^(([\+]\d{1,2})?(\s?[\(]\d{1,2}[\)]\s?)?((\d{1})?[\(]\d{1,3}[\)])?(\d{3}[-]\d{4})?((\d{1,3}\s)+\d{4})*(\d{5,9})?(\d{5}[.]\d{5})?)$",value)

	if matchname or matchno:
		print("Input Validated")
		try:
			curConn = Conn.cursor()
			curConn.execute("""select * from secprj where name = %s or phonenumber = %s""",(value,value))
			result = curConn.fetchone()
			curConn.execute("""delete from secprj where name = %s or phonenumber = %s""", (value,value))
			Conn.commit()	
	
			if result is None:
				sys.stderr.write("No rows were deleted - Record not found")
				sys.exit(1)
			else:
				sys.stderr.write("The record was deleted")
				sys.exit(0)
		
		finally:
			Conn.close()
		sys.exit(1)		
	else:
		sys.stderr.write("Invalid input. Please try again")
		sys.exit(1)

if __name__ == "__main__":
    main()