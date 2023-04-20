import mysql.connector
import re
import os
from tabulate import tabulate

# FUNCTIONS TO BE USED IN PROGRAM
# checks if a string is in the format YYYY-MM-DD
def checkDateFormat(dateString):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, dateString))

# checks if a string is in email format
def checkEmailFormat(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# CONNECT TO DATABASE
mydb = mysql.connector.connect(
    host = "db4free.net",
    user = "zeinnoureddin",
    password = "admin123",
    database = "carmarketplace"
)

# MAIN MENU
print("Welcome to Car Marketplace\nPlease select an option from the menu below:")
print("1. Register a user")
print("2. Login")
print("3. Exit")

menuOption = input()
os.system('cls')

mycursor = mydb.cursor()

# REGISTER A USER
if menuOption == "1":
    # get username
    print("Please enter a username: ")
    username = input()
    while len(username) > 30 or len(username) < 6:
        print("This is not a valid input. Please enter a username between 6 and 30 characters: ")
        username = input()
        os.system('cls')

    # get email and check if it is unique
    print("Please enter your email address: ")
    userEmail = input()
    os.system('cls')
    while len(userEmail) > 325:
        print("This is not a valid input. The length of the email address should not exceed 325 characters. Please try again: ")
        userEmail = input()
        os.system('cls')

    while not checkEmailFormat(userEmail):
        print("This is not a valid input. Please enter a valid email address: ")
        userEmail = input()
        os.system('cls')
    isEmailUnique = """
    SELECT emailAddress FROM marketuser WHERE emailAddress = '%s'
    """ % (userEmail)
    mycursor.execute(isEmailUnique)
    test = mycursor.fetchall()
    while test != []:
        print("This email is already registered. Please enter a different email address.")
        userEmail = input()
        os.system('cls')
        isEmailUnique = """
        SELECT emailAddress FROM marketuser WHERE emailAddress = '%s'
        """ % (userEmail)
        mycursor.execute(isEmailUnique)
        test = mycursor.fetchall()

    # get gender
    print("Please enter your gender. Enter M for male and F for female: ")
    userGender = input()
    os.system('cls')
    while userGender != "M" and userGender != "F":
        print("This is not a valid input. Please enter M for male and F for female: ")
        userGender = input()
        os.system('cls')

    # get birthdate
    print("Please enter your birthdate in the format YYYY-MM-DD: ")
    userBirthdate = input()
    os.system('cls')
    while not checkDateFormat(userBirthdate):
        print("This is not a valid input. Please enter your birthdate in the format YYYY-MM-DD: ")
        userBirthdate = input()
        os.system('cls')

    # add the user to the database
    addUser = """
    INSERT INTO marketuser
    VALUES ('%s', '%s', '%s', '%s');
    """ % (userEmail, username, userGender, userBirthdate)
    mycursor.execute(addUser)
    mydb.commit()

# LOGIN
elif menuOption == "2":
    print("Please enter your email address: ")
    userEmail = input()
    os.system('cls')
    doesEmailExist = """
    SELECT emailAddress FROM marketuser WHERE emailAddress = '%s'
    """ % (userEmail)
    mycursor.execute(doesEmailExist)
    test = mycursor.fetchall()
    while test == []:
        print("This email is not registered. Make sure that you're writing the correct email address.")
        userEmail = input()
        os.system('cls')
        doesEmailExist = """
        SELECT emailAddress FROM marketuser WHERE emailAddress = '%s'
        """ % (userEmail)
        mycursor.execute(doesEmailExist)
        test = mycursor.fetchall()
    print("You have successfully logged in.")

exitQueryMenu = False
showBigMenu = True
while not exitQueryMenu:
    # QUERY MENU
    if showBigMenu:
        print("Please select a query option from the menu below:")
        print("1. Add a new sale for an ad")
        print("2. View existing reviews of a given ad")
        print("3. View aggregated rating of a seller / owner")
        print("4. Show all the ads for a given car make, body type and year in a specific location / area, along with the average price the number of listings for each model")
        print("5. Show all the used cars in a certain location in a given price range, with a given set of features")
        print("6. Show the top 5 areas in cairo by amount of inventory and average price a given make / model")
        print("7. Show the top 5 sellers by the amount of listings they have, along with their avg price per year")
        print("8. Show all the properties listed by a specific owner (given their first and last name and / or phone no)")
        print("9. Show the top 5 make / models cars by the amount of inventory and their average price for a given year range")
        print("10. Exit")
        queryOption = input()
        os.system('cls')
        showBigMenu = False
    else:
        print("Please select one of the following options:")
        print("1. Run another query")
        print("2. Exit")
        exitOrStay = input()
        os.system('cls')
        showBigMenu = True
        if exitOrStay == "2":
            exitQueryMenu = True
        continue

    if queryOption == "1":
        print("Please enter the ad ID: ")
        adID = input()
        os.system('cls')

        doesIDExist = """
        SELECT AdID FROM ad WHERE AdID = '%s'
        """ % (adID)
        mycursor.execute(doesIDExist)
        test = mycursor.fetchall()

        isThereSale = """
        SELECT AdID FROM sale WHERE AdID = '%s'
        """ % (adID)
        mycursor.execute(isThereSale)
        test2 = mycursor.fetchall()

        while test == [] or test2 != []:
            if test == []:
                print("This ID does not exist. Please enter a valid ID.")
                adID = input()
                os.system('cls')
                doesIDExist = """
                SELECT AdID FROM ad WHERE AdID = '%s'
                """ % (adID)
                mycursor.execute(doesIDExist)
                test = mycursor.fetchall()
                isThereSale = """
                SELECT AdID FROM sale WHERE AdID = '%s'
                """ % (adID)
                mycursor.execute(isThereSale)
                test2 = mycursor.fetchall()
            if test2 != []:
                print("There is already a sale for this ad. Please enter a different ad ID.")
                adID = input()
                os.system('cls')
                doesIDExist = """
                SELECT AdID FROM ad WHERE AdID = '%s'
                """ % (adID)
                mycursor.execute(doesIDExist)
                test = mycursor.fetchall()
                isThereSale = """
                SELECT AdID FROM sale WHERE AdID = '%s'
                """ % (adID)
                mycursor.execute(isThereSale)
                test2 = mycursor.fetchall()
                
        print("Please enter the selling price of the car: ")
        sellingPrice = input()
        os.system('cls')
        while not sellingPrice.isdigit():
            print("This is not a valid input. Please enter a valid selling price.")
            sellingPrice = input()
            os.system('cls')
        print("Please enter your review:")
        review = input()
        os.system('cls')
        while len(review) > 1500: 
            print("The character count in the review shouldn't exceed 1500. Please try again.")
            review = input()
            os.system('cls')
        print("On a scale of 1 to 5, please give a rating to the selling process and the car:")
        rating = input()
        os.system('cls')
        while not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            print("This is not a valid input. Please make sure that you're entering a number between 1 and 5.")
            rating = input()
            os.system('cls')
        addSale = """
        INSERT INTO sale
        VALUES ('%s', '%s', '%s', '%s', '%s');
        """ % (sellingPrice, review, rating, adID, userEmail)
        mycursor.execute(addSale)
        mydb.commit()
        print("You have successfully added a new sale for this ad.")

    elif queryOption == "2":
        print("Please enter the ad ID: ")
        adID = input()
        os.system('cls')
        doesIDExist = """
        SELECT AdID FROM sale WHERE AdID = '%s'
        """ % (adID)
        mycursor.execute(doesIDExist)
        test = mycursor.fetchall()
        while test == []:
            print("This ID does not have a sale. Please enter a valid ID.")
            adID = input()
            os.system('cls')
            doesIDExist = """
            SELECT AdID FROM sale WHERE AdID = '%s'
            """ % (adID)
            mycursor.execute(doesIDExist)
            test = mycursor.fetchall()
        viewReviews = """
        SELECT review FROM sale WHERE AdID = '%s'
        """ % (adID)
        mycursor.execute(viewReviews)
        result = mycursor.fetchall()
        print("Ad review: " + result[0][0])

    elif queryOption == "3":
        print("Please enter the seller's name: ")
        sellerName = input()
        os.system('cls')
        print("Please enter the seller's phone number: ")
        sellerPhone = input()
        os.system('cls')
        doesSellerExist = """
        SELECT OwnerName, OwnerPhoneNumber FROM adowner WHERE OwnerName = '%s' AND OwnerPhoneNumber = '%s'
        """ % (sellerName, sellerPhone)
        mycursor.execute(doesSellerExist)
        test = mycursor.fetchall()
        while test == []:
            print("This seller does not exist. Make sure you're entering the correct name and phone number.")
            print("Enter seller's name: ")
            sellerName = input()
            os.system('cls')
            print("Enter seller's phone number: ")
            sellerPhone = input()
            os.system('cls')
            doesSellerExist = """
            SELECT OwnerName, OwnerPhoneNumber FROM adowner WHERE OwnerName = '%s' AND OwnerPhoneNumber = '%s'
            """ % (sellerName, sellerPhone)
            mycursor.execute(doesSellerExist)
            test = mycursor.fetchall()
        viewSellerRating = """
        SELECT AVG(Rating)
        FROM sale S INNER JOIN ad AD ON S.AdID = AD.AdID INNER JOIN adowner AO ON AD.OwnerPhoneNumber = AO.OwnerPhoneNumber AND AD.OwnerName = AO.OwnerName
        WHERE AO.OwnerName = '%s' AND AO.OwnerPhoneNumber = '%s';
        """ % (sellerName, sellerPhone)
        mycursor.execute(viewSellerRating)
        result = mycursor.fetchall()
        if result[0][0] == None:
            print("This seller does not have a rating yet.")
        else: 
            print("The seller's rating is: " + str(result[0][0]))

    elif queryOption == "4":
        print("Please enter the car make: ")
        carMake = input()
        os.system('cls')
        print("Please enter the car body type: ")
        carBodyType = input()
        os.system('cls')
        print("Please enter the car year: ")
        carYear = input()
        os.system('cls')
        while not carYear.isdigit():
            print("This is not a valid input. Please enter a valid year.")
            carYear = input()
            os.system('cls')
        print("Please enter the location: ")
        location = input()
        os.system('cls')
        doesCarExist = """
        SELECT Model, Count(*) AS Listings, AVG(Price) AS ModelAveragePrice
        FROM ad
        WHERE Brand = '%s' AND BodyType = '%s' AND ModelYear = '%s' AND Location = '%s'
        GROUP BY 1;
        """ % (carMake, carBodyType, carYear, location)
        mycursor.execute(doesCarExist)
        result = mycursor.fetchall()
        if result[0][0] == None:
            print("There are no such ads.")
        else:
            table = [['Model', 'Listings', 'ModelAveragePrice']]
            for r in result:
                table.append([r[0], r[1], r[2]])
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    elif queryOption == "5":
        print("Please enter the location: ")
        location = input()
        os.system('cls')
        print("Please enter the minimum price: ")
        minPrice = input()
        os.system('cls')
        while not minPrice.isdigit():
            print("This is not a valid input. Please enter a valid price.")
            minPrice = input()
            os.system('cls')
        print("Please enter the maximum price: ")
        maxPrice = input()
        os.system('cls')
        while not maxPrice.isdigit():
            print("This is not a valid input. Please enter a valid price.")
            maxPrice = input()
            os.system('cls')
        print("Please enter the features you want to search for, separated by a comma. Please make sure not to add spaces after the commas: ")
        features = input()
        os.system('cls')
        features = features.replace(",", "','")
        features = "'" + features + "'"
        query = f"""
        SELECT ad.AdID, ad.Price, ad.PaymentOption, ad.MinKilometers, ad.MaxKilometers, ad.CarCondition, ad.BodyType, ad.FuelType, ad.PriceType, ad.Color, ad.MinEngineCapacity, ad.MaxEngineCapacity, ad.Location, ad.Brand, ad.Model, ad.ModelYear, ad.TransmissionType, ad.ownerPhoneNumber, ad.ownerName
        FROM ad INNER JOIN adextrafeatures aef ON ad.AdID = aef.AdID
        WHERE ad.Location = '{location}' AND ad.Price >= '{minPrice}' AND ad.Price <= '{maxPrice}' AND aef.extraFeature IN ({features})
        GROUP BY ad.AdID, ad.Price, ad.PaymentOption, ad.MinKilometers, ad.MaxKilometers, ad.CarCondition, ad.BodyType, ad.FuelType, ad.PriceType, ad.Color, ad.MinEngineCapacity, ad.MaxEngineCapacity, ad.Location, ad.Brand, ad.Model, ad.ModelYear, ad.TransmissionType, ad.ownerPhoneNumber, ad.ownerName
        HAVING COUNT(DISTINCT aef.extraFeature) = '{len(features.split(","))}';
        """
        mycursor.execute(query)
        result = mycursor.fetchall()
        if result[0][0] == None:
            print("There are no such cars.")
        else:
            table = [['AdID', 'Price', 'PaymentOption', 'MinKilometers', 'MaxKilometers', 'CarCondition', 'BodyType', 'FuelType', 'PriceType', 'Color', 'MinEngineCapacity', 'MaxEngineCapacity', 'Location', 'Brand', 'Model', 'ModelYear', 'TransmissionType', 'ownerPhoneNumber', 'ownerName']]
            for r in result:
                table.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18]])
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    
    elif queryOption == "6":    
        print("Please enter the car make: ")
        carMake = input()
        os.system('cls')
        print("Please enter the car model: ")
        carModel = input()
        os.system('cls')
        query = f"""
        SELECT Location, COUNT(*) AS InventoryCount, AVG(Price) AS AveragePrice
        FROM ad
        WHERE Brand = '{carMake}' AND Model = '{carModel}'
        GROUP BY 1
        ORDER BY 2 DESC, 3 DESC
        LIMIT 5;
        """
        mycursor.execute(query)
        result = mycursor.fetchall()
        if result[0][0] == None:
            print("There are no such areas.")
        else:
            table = [['Location', 'InventoryCount', 'AveragePrice']]
            for r in result:
                table.append([r[0], r[1], r[2]])
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    elif queryOption == "7":
        query = """	
        SELECT OwnerName, OwnerPhoneNumber, COUNT(*) AS ListingsAmount, AVG(Price) AS AveragePrice
        FROM ad 
        GROUP BY 1, 2
        ORDER BY 3 DESC
        LIMIT 5; 
        """
        mycursor.execute(query)
        result = mycursor.fetchall()
        table = [['OwnerName', 'OwnerPhoneNumber', 'Count', 'AveragePrice']]
        for r in result:
            table.append([r[0], r[1], r[2], r[3]])
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    
    elif queryOption == "8":
        print("Please enter the owner's name: ")
        ownerName = input()
        os.system('cls')
        print("Please enter the owner's phone number: ")
        ownerPhoneNumber = input()
        os.system('cls')
        query = f"""
        SELECT OwnerName
        FROM adowner
        WHERE OwnerName = '{ownerName}' AND OwnerPhoneNumber = '{ownerPhoneNumber}';
        """
        mycursor.execute(query)
        test = mycursor.fetchall()
        while test == []:
            print("There does not exist such an owner. Please make sure you have entered the correct information")
            print("Please enter the owner's name: ")
            ownerName = input()
            os.system('cls')
            print("Please enter the owner's phone number: ")
            ownerPhoneNumber = input()
            os.system('cls')
            query = f"""
            SELECT OwnerName
            FROM adowner
            WHERE OwnerName = '{ownerName}' AND OwnerPhoneNumber = '{ownerPhoneNumber}';
            """
            mycursor.execute(query)
            test = mycursor.fetchall()
        # DID NOT PRINT DESCRIPTION BECAUSE IT RUINS THE TABLE
        query = f"""
        SELECT AdID, Price, PaymentOption, MinKilometers, MaxKilometers, CarCondition, BodyType, FuelType, PriceType, Color, MinEngineCapacity, MaxEngineCapacity, Location, Brand, Model, ModelYear, TransmissionType, ownerPhoneNumber, ownerName
        FROM ad
        WHERE OwnerName = '{ownerName}' AND OwnerPhoneNumber = '{ownerPhoneNumber}';
        """
        mycursor.execute(query)
        result = mycursor.fetchall()
        table = [['AdID', 'Price', 'PaymentOption', 'MinKilometers', 'MaxKilometers', 'CarCondition', 'BodyType', 'FuelType', 'PriceType', 'Color', 'MinEngineCapacity', 'MaxEngineCapacity', 'Location', 'Brand', 'Model', 'ModelYear', 'TransmissionType', 'ownerPhoneNumber', 'ownerName']]
        for r in result:
            table.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18]])
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    # Show the top 5 make / models cars by the amount of inventory and their average price for a given year range
    elif queryOption == "9":
        print("Please enter the start year: ")
        startYear = input()
        while not startYear.isdigit():
            print("Please enter a valid year.")
            startYear = input()
        os.system('cls')
        print("Please enter the end year: ")
        endYear = input()
        while not endYear.isdigit():
            print("Please enter a valid year.")
            endYear = input()
        os.system('cls')
        query = f"""
        SELECT Brand, Model, COUNT(*) AS InventoryCount, AVG(Price) AS AveragePrice
        FROM ad
        WHERE ModelYear BETWEEN '{startYear}' AND '{endYear}'
        GROUP BY 1, 2
        ORDER BY InventoryCount DESC, AveragePrice DESC
        LIMIT 5;
        """
        mycursor.execute(query)
        result = mycursor.fetchall()
        table = [['Brand', 'Model', 'InventoryCount', 'AveragePrice']]
        for r in result:
            table.append([r[0], r[1], r[2], r[3]])
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
            
    elif queryOption == "10":
        exitQueryMenu = True