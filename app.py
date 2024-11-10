from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Student@123",  # Replace with your MySQL password
            database="wardrobe"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create MySQL table if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        gender VARCHAR(10),
        working_professional CHAR(20),
        number_of_clothes INT,
        wardrobe_size INT,
        number_of_sections INT,
        clothes_type VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()

# Insert data to MySQL
def insert_user_data(connection, user_data):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user (name, age, gender, working_professional, number_of_clothes, wardrobe_size, number_of_sections, clothes_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, user_data)
    connection.commit()

# Handle chatbot conversation and wardrobe logic
@app.route('/wardrobe', methods=['POST'])
def wardrobe():
    user_input = request.json
    name = user_input['name']
    age = int(user_input['age'])
    gender = user_input['gender']
    working_professional = user_input['working_professional']
    number_of_clothes = int(user_input['number_of_clothes'])
    wardrobe_size = int(user_input['wardrobe_size'])
    number_of_sections = int(user_input['number_of_sections'])
    clothes_type = user_input['clothes_type']

    # Store data in the database
    connection = connect_to_database()
    create_table(connection)
    user_data = (name, age, gender, working_professional == 'Yes', number_of_clothes, wardrobe_size, number_of_sections, clothes_type)
    insert_user_data(connection, user_data)
    connection.close()

    # Provide wardrobe advice based on number of clothes
    advice = ""
    if number_of_clothes < 10:
        advice = """Minimalist Wardrobe: With fewer than 10 clothes, you should focus on keeping versatile, high-quality items that can be mixed and matched for different occasions.
Recommendation:
Hanging Clothes: If you have formal attire like blazers or dresses, hang them neatly to prevent wrinkles.

Folded Clothes: Fold casual clothes like T-shirts and jeans. Place them in a drawer or on a shelf for easy access.

Accessories & Shoes: Store accessories like belts, ties, and shoes in a designated section. Since you have fewer items, a single drawer or shelf should suffice.

Tip: Opt for a compact arrangement. Roll up clothes for space efficiency and make the most of multi-purpose items (e.g., a jacket that works for both casual and formal settings)."""
    elif 10 <= number_of_clothes <= 30:
        advice = """Basic Segregation and Organization: With a moderate number of clothes, it’s time to begin organizing by type and frequency of use.
Recommendation:

Hanging Clothes: Use this space for items that wrinkle easily, such as formal shirts, dresses, blazers, and lightweight jackets.

Folded Clothes: Stack casual tops, jeans, sweaters, and workout clothes. You can fold them and categorize by season or activity (e.g., work, casual, gym).

Accessories & Shoes: Create a small section for your accessories like scarves, hats, belts, and shoes. Consider using hooks or small boxes for accessories.

Tip: A wardrobe organizer with dividers can help you keep track of different categories of clothes. Rotate clothes seasonally for easier access."""
    elif 30 < number_of_clothes <= 50:
        advice = """Seasonal Rotation & Outfit Planning: When you have 30–50 clothes, it’s essential to segregate based on season, type, and purpose (work, casual, special occasions).

Recommendation:

Hanging Clothes: Hang formal and delicate items such as blouses, dresses, and suits. Consider separating work clothes from casual or going-out outfits.

Folded Clothes: Create categories for folded clothes, such as casual wear, office wear, and seasonal clothing. Fold sweaters and bulkier items on lower shelves.

Shoes & Accessories: Consider shoe racks or stacking shoe boxes. Use organizers or boxes for accessories, with a separate space for jewelry or belts.

Sections: Use separate sections for each category of clothes (formal, casual, workout) and label them. You can also organize by color for aesthetic appeal.

Tip: Rotate clothes according to season. Store winter clothes during summer, and vice versa, to free up space."""
    elif 50 < number_of_clothes <= 70:
        advice = """Color Coding & Detailed Categorization: At this stage, space management is key. Introduce further segregation based on usage, frequency, and occasion.

Recommendation:

Hanging Clothes: Dedicate one side of the wardrobe to formal or work clothes and the other side to casual and occasional wear. Consider hanging based on outfits (e.g., complete outfits for workdays).

Folded Clothes: Create specific stacks for gym wear, casuals, and loungewear. Use drawer dividers to keep everything neatly segmented.

Shoes & Accessories: Create a dedicated section for shoes and accessories. Use stackable boxes or racks for shoes. For accessories, try drawer inserts to keep items like belts, ties, and scarves in order.

Sections: Add labeled sections for day-to-day clothes, seasonal wear, and special occasion outfits. Make sure each type has a designated spot.

Tip: Optimize space with vertical storage solutions, such as double hanging rods or using hooks on the wardrobe doors for bags, hats, or scarves."""
    elif 70 < number_of_clothes <= 100:
        advice = """Detailed Sorting by Occasion and Use Frequency: With a large number of clothes, careful segregation by category and occasion is critical for an organized and functional wardrobe.

Recommendation:
Hanging Clothes: Group clothes by occasion (formal, casual, semi-formal, etc.) and then by type (shirts, jackets, dresses). Alternatively, you could sort by color for a visually appealing and easier-to-navigate wardrobe.

Folded Clothes: Keep a dedicated drawer or shelf for each category—tops, bottoms, sweaters, loungewear, etc. For frequently used clothes, place them at the top of each pile.

Shoes & Accessories: Dedicate a section of your wardrobe to shoes (organized by type or frequency of use) and accessories. Use an accessory tray or box for smaller items like jewelry, watches, or belts.

Sections: Consider creating seasonal sections for summer and winter clothes, and separate formal wear from casual attire. If you have limited space, store off-season clothes in containers or under-bed storage.

Tip: Invest in wardrobe organizers such as hanging shelves or cascading hangers to maximize vertical space. Periodically assess your wardrobe to remove clothes you no longer use."""
    else:
        advice = """Percentage-based Categorization: At this level, a structured approach is vital to avoid clutter and ensure every item is accessible. You should organize clothes in percentage-wise sections based on categories like work, casual, special occasions, and seasonal.
        
Recommendation:
Hanging Clothes: Allocate 30-40% of the hanging space to workwear (suits, shirts, dresses), 20-30% to casual or daily wear, and the remaining for special occasion outfits. Separate clothes by type and sub-categorize based on season or color.

Folded Clothes: Stack by clothing category and sub-categorize based on frequency of use. For example, allocate 20% of the space for loungewear, 30% for gym wear, 40% for casual tops, and the rest for sweaters or off-season items.

Shoes & Accessories: Dedicate specific percentages of your wardrobe for shoes and accessories. For example, 10-15% for shoes and 5-10% for accessories like belts, scarves, and hats. Use shoe racks, boxes, and hooks.

Sections: Clearly define sections for categories such as work, casual, sports, and special occasions. Each section can also have a seasonal sub-section to make it easier to rotate clothes.

Tip: Consider seasonal rotation as well as a regular decluttering process. Items that you haven’t worn in a year should be reviewed for donation or storage."""

    return jsonify({"advice": advice})

# Render chatbot HTML page
@app.route('/')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
