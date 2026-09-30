#!/usr/bin/env python3
"""Builds web/modules/custom/meilisearch_demo/data/recipes.json.

The recipes are written for this demo. Each line:
title | cuisine | meal types | minutes | rating | emoji | diets | description | ingredients
Diets: V vegetarian, VG vegan, GF gluten-free.
"""
import json
import pathlib

RECIPES = """
Margherita Pizza|Italian|Dinner,Lunch|45|4.7|🍕|V|A thin, blistered crust with San Marzano tomatoes, fresh mozzarella and basil: the pizza Naples is proud of.|pizza dough;San Marzano tomatoes;fresh mozzarella;basil;olive oil;sea salt
Spaghetti Carbonara|Italian|Dinner|25|4.8|🍝||Silky egg and pecorino sauce clinging to spaghetti, with crisp guanciale and plenty of black pepper. No cream, ever.|spaghetti;guanciale;egg yolks;pecorino romano;black pepper
Mushroom Risotto|Italian|Dinner|40|4.5|🍚|V,GF|Creamy arborio rice slowly stirred with porcini stock and finished with butter and parmesan.|arborio rice;porcini mushrooms;shallot;white wine;vegetable stock;parmesan;butter
Lasagna alla Bolognese|Italian|Dinner|180|4.9|🍝||Layers of fresh pasta, slow-cooked beef ragù and nutmeg béchamel baked until bubbling.|lasagna sheets;ground beef;pork;tomato passata;milk;butter;flour;nutmeg;parmesan
Pesto Genovese Trofie|Italian|Lunch,Dinner|20|4.6|🌿|V|Twisted trofie pasta tossed with bright basil pesto, potatoes and green beans, the Ligurian way.|trofie;basil;pine nuts;garlic;parmesan;olive oil;potatoes;green beans
Tiramisu|Italian|Dessert|30|4.8|🍰|V|Espresso-soaked ladyfingers layered with mascarpone cream and a dusting of cocoa. Better the next day.|ladyfingers;espresso;mascarpone;eggs;sugar;cocoa powder;marsala
Caprese Salad|Italian|Lunch,Snack|10|4.3|🍅|V,GF|Ripe tomatoes, creamy mozzarella and basil with good olive oil. Summer on a plate.|tomatoes;mozzarella;basil;olive oil;balsamic vinegar;sea salt
Minestrone|Italian|Lunch,Dinner|60|4.4|🥣|VG|A hearty vegetable soup with beans and small pasta, even better with a spoon of pesto.|cannellini beans;carrots;celery;zucchini;tomatoes;ditalini;onion;garlic
Osso Buco|Italian|Dinner|150|4.7|🍖|GF|Veal shanks braised in white wine and tomato until they fall apart, topped with bright gremolata.|veal shanks;white wine;tomatoes;carrots;celery;lemon zest;parsley;garlic
Focaccia|Italian|Snack,Lunch|240|4.6|🍞|VG|A dimpled, golden flatbread with rosemary, flaky salt and a generous pour of olive oil.|bread flour;yeast;olive oil;rosemary;flaky salt
Panna Cotta|Italian|Dessert|20|4.5|🍮|V,GF|A trembling vanilla cream set with a little gelatin, served with a berry coulis.|cream;milk;sugar;vanilla;gelatin;raspberries
Cacio e Pepe|Italian|Dinner|15|4.6|🧀|V|Three ingredients, one technique: pecorino and pepper emulsified into a glossy sauce.|tonnarelli;pecorino romano;black pepper
Chicken Tacos al Pastor|Mexican|Dinner|50|4.7|🌮|GF|Chicken marinated in chilies and pineapple, charred and tucked into warm corn tortillas.|chicken thighs;guajillo chilies;pineapple;achiote;corn tortillas;onion;cilantro;lime
Guacamole|Mexican|Snack|10|4.8|🥑|VG,GF|Chunky avocado with lime, onion, jalapeño and cilantro. Made right before serving.|avocados;lime;red onion;jalapeño;cilantro;salt
Chiles Rellenos|Mexican|Dinner|60|4.4|🌶️|V|Roasted poblano peppers stuffed with cheese, dipped in a light batter and fried.|poblano peppers;queso oaxaca;eggs;flour;tomato sauce
Black Bean Burrito Bowl|Mexican|Lunch|25|4.3|🥙|VG,GF|Cilantro-lime rice, spiced black beans, corn salsa and avocado in one colorful bowl.|rice;black beans;corn;tomatoes;avocado;lime;cilantro;cumin
Chicken Enchiladas Verdes|Mexican|Dinner|55|4.6|🫔|GF|Corn tortillas rolled around shredded chicken and baked under a tangy tomatillo sauce.|corn tortillas;chicken;tomatillos;serrano chilies;crema;queso fresco
Churros with Chocolate|Mexican|Dessert,Snack|35|4.7|🍫|V|Crisp, cinnamon-sugar churros with a thick hot chocolate for dipping.|flour;butter;eggs;cinnamon;sugar;dark chocolate;milk
Pozole Rojo|Mexican|Dinner|180|4.5|🍲|GF|A festive pork and hominy stew in a deep red chili broth, topped with radish and cabbage.|pork shoulder;hominy;guajillo chilies;ancho chilies;garlic;radish;cabbage;oregano
Huevos Rancheros|Mexican|Breakfast|20|4.5|🍳|V,GF|Fried eggs on crisp tortillas with ranchero sauce, beans and a little crumbled cheese.|eggs;corn tortillas;tomatoes;jalapeño;refried beans;queso fresco
Elote|Mexican|Snack|15|4.6|🌽|V,GF|Grilled corn on the cob slathered with mayo, cotija, chili powder and lime.|corn on the cob;mayonnaise;cotija;chili powder;lime
Fish Tacos Baja|Mexican|Lunch,Dinner|30|4.6|🐟||Beer-battered white fish with crunchy cabbage slaw and chipotle crema.|white fish;flour;beer;cabbage;chipotle;crema;tortillas;lime
Tres Leches Cake|Mexican|Dessert|90|4.7|🎂|V|A light sponge soaked in three milks and crowned with whipped cream.|flour;eggs;sugar;evaporated milk;condensed milk;cream;vanilla
Horchata|Mexican|Drink|15|4.4|🥛|VG,GF|A chilled rice and cinnamon drink, sweet and refreshing.|rice;cinnamon;sugar;vanilla;almond milk
Chicken Ramen|Japanese|Dinner|120|4.8|🍜||Rich chicken broth, springy noodles, a jammy soy egg and tender chashu chicken.|chicken bones;ramen noodles;soy sauce;mirin;eggs;scallions;nori;ginger
Salmon Nigiri|Japanese|Lunch,Dinner|60|4.7|🍣|GF|Seasoned sushi rice shaped by hand and topped with fresh salmon.|sushi rice;rice vinegar;salmon;wasabi;tamari
Miso Soup|Japanese|Breakfast,Lunch|15|4.4|🥣|VG|A comforting dashi broth with miso, silken tofu, wakame and scallions.|kombu;miso paste;silken tofu;wakame;scallions
Chicken Katsu Curry|Japanese|Dinner|50|4.7|🍛||Crisp panko chicken cutlet on rice with a mellow, sweet Japanese curry sauce.|chicken breast;panko;eggs;curry roux;onion;carrots;potatoes;rice
Okonomiyaki|Japanese|Lunch,Dinner|30|4.5|🥞||A savory cabbage pancake with pork belly, drizzled with okonomi sauce and mayo.|cabbage;flour;eggs;dashi;pork belly;okonomi sauce;kewpie mayo;bonito flakes
Vegetable Tempura|Japanese|Snack,Dinner|30|4.4|🍤|VG|Feather-light batter around sweet potato, eggplant and shiso, with a dipping sauce.|sweet potato;eggplant;shiso;flour;ice water;tentsuyu sauce
Matcha Cheesecake|Japanese|Dessert|300|4.6|🍵|V|A jiggly, cloud-soft cheesecake with the gentle bitterness of matcha.|cream cheese;eggs;sugar;matcha;milk;flour;butter
Teriyaki Salmon|Japanese|Dinner|20|4.6|🐟|GF|Pan-seared salmon glazed with a glossy homemade teriyaki sauce.|salmon;tamari;mirin;sake;sugar;ginger;sesame seeds
Onigiri|Japanese|Snack,Lunch|25|4.3|🍙|GF|Rice triangles wrapped in nori with salmon, umeboshi or tuna mayo inside.|sushi rice;nori;salmon;umeboshi;tuna;salt
Gyoza|Japanese|Snack,Dinner|60|4.7|🥟||Pork and cabbage dumplings, crisp on the bottom and steamed on top.|gyoza wrappers;ground pork;cabbage;garlic;ginger;soy sauce;sesame oil
Yakitori|Japanese|Dinner,Snack|40|4.5|🍢|GF|Chicken skewers grilled over charcoal and brushed with tare.|chicken thighs;scallions;tamari;mirin;sake;sugar
Mochi Ice Cream|Japanese|Dessert|45|4.4|🍡|V,GF|Soft, chewy rice dough wrapped around balls of ice cream.|glutinous rice flour;sugar;cornstarch;ice cream
Butter Chicken|Indian|Dinner|60|4.9|🍛|GF|Tandoori chicken simmered in a velvety tomato, butter and cream sauce.|chicken thighs;yogurt;garam masala;tomatoes;butter;cream;fenugreek;garlic;ginger
Chana Masala|Indian|Lunch,Dinner|40|4.6|🫘|VG,GF|Chickpeas in a tangy, spiced tomato and onion gravy.|chickpeas;onion;tomatoes;chana masala;ginger;garlic;cilantro
Palak Paneer|Indian|Dinner|35|4.6|🥬|V,GF|Cubes of paneer in a smooth, garlicky spinach sauce.|paneer;spinach;onion;garlic;ginger;cream;garam masala
Chicken Biryani|Indian|Dinner|90|4.8|🍚|GF|Fragrant basmati layered with spiced chicken, saffron and crispy onions.|basmati rice;chicken;yogurt;saffron;fried onions;mint;biryani masala
Masala Dosa|Indian|Breakfast,Lunch|45|4.7|🥞|VG,GF|A crisp fermented rice crepe filled with spiced potatoes, served with chutney.|dosa batter;potatoes;mustard seeds;curry leaves;turmeric;coconut chutney
Dal Tadka|Indian|Dinner,Lunch|35|4.5|🍲|VG,GF|Yellow lentils finished with a sizzling tempering of cumin, garlic and chili.|toor dal;cumin seeds;garlic;dried chilies;tomatoes;turmeric;ghee
Samosas|Indian|Snack|60|4.6|🥟|VG|Flaky pastry triangles stuffed with spiced potatoes and peas.|flour;potatoes;peas;cumin;coriander;green chilies;oil
Mango Lassi|Indian|Drink,Breakfast|5|4.7|🥭|V,GF|A thick, chilled blend of ripe mango, yogurt and a pinch of cardamom.|mango;yogurt;milk;sugar;cardamom
Aloo Gobi|Indian|Lunch,Dinner|35|4.3|🥔|VG,GF|Potatoes and cauliflower roasted with turmeric, cumin and fresh ginger.|potatoes;cauliflower;turmeric;cumin;ginger;cilantro
Gulab Jamun|Indian|Dessert|50|4.6|🍩|V|Soft milk dumplings soaked in rose and cardamom syrup.|milk powder;flour;ghee;sugar;rose water;cardamom
Lamb Rogan Josh|Indian|Dinner|120|4.7|🍖|GF|Tender lamb in a deep red Kashmiri chili and yogurt sauce.|lamb shoulder;kashmiri chili;yogurt;fennel;ginger;cardamom;cloves
Masala Chai|Indian|Drink,Breakfast|10|4.5|☕|V,GF|Black tea brewed with milk, ginger and warm spices.|black tea;milk;ginger;cardamom;cinnamon;cloves;sugar
Croissants|French|Breakfast|720|4.8|🥐|V|Buttery, flaky, laminated pastry worth every minute of the wait.|flour;butter;milk;yeast;sugar;salt
Coq au Vin|French|Dinner|150|4.7|🍗|GF|Chicken braised in red wine with mushrooms, pearl onions and bacon.|chicken;red wine;mushrooms;pearl onions;bacon;thyme;garlic
Ratatouille|French|Lunch,Dinner|70|4.5|🍆|VG,GF|Provençal summer vegetables slowly stewed with herbs and olive oil.|eggplant;zucchini;bell peppers;tomatoes;onion;garlic;thyme;basil
French Onion Soup|French|Dinner,Lunch|90|4.6|🧅||Deeply caramelized onions in beef broth under a lid of toasted bread and gruyère.|onions;beef stock;white wine;baguette;gruyère;butter;thyme
Crêpes|French|Breakfast,Dessert|30|4.6|🥞|V|Thin, lacy pancakes with butter and sugar, jam or chocolate.|flour;eggs;milk;butter;sugar
Quiche Lorraine|French|Lunch|75|4.5|🥧||A crisp pastry shell filled with smoky bacon and a silky egg custard.|shortcrust pastry;bacon;eggs;cream;gruyère;nutmeg
Beef Bourguignon|French|Dinner|210|4.8|🍷|GF|Beef slowly braised in Burgundy wine with carrots, mushrooms and onions.|beef chuck;red wine;carrots;mushrooms;pearl onions;bacon;thyme;bay leaf
Crème Brûlée|French|Dessert|60|4.8|🍮|V,GF|Cold vanilla custard under a crackly caramelized sugar crust.|cream;egg yolks;sugar;vanilla bean
Salade Niçoise|French|Lunch|25|4.4|🥗|GF|Tuna, eggs, olives, green beans and potatoes with a mustardy vinaigrette.|tuna;eggs;olives;green beans;potatoes;tomatoes;anchovies;dijon mustard
Croque Monsieur|French|Lunch|20|4.4|🥪||A toasted ham and gruyère sandwich smothered in béchamel.|bread;ham;gruyère;butter;flour;milk;dijon mustard
Tarte Tatin|French|Dessert|75|4.7|🍎|V|Upside-down caramelized apple tart with buttery pastry.|apples;butter;sugar;puff pastry
Moules Marinières|French|Dinner|25|4.5|🦪|GF|Mussels steamed in white wine, shallots and parsley. Bread for the broth.|mussels;white wine;shallots;garlic;parsley;butter
Pad Thai|Thai|Dinner,Lunch|30|4.7|🍜|GF|Stir-fried rice noodles with tamarind, shrimp, egg, peanuts and lime.|rice noodles;shrimp;eggs;tamarind;fish sauce;palm sugar;bean sprouts;peanuts;lime
Green Curry|Thai|Dinner|35|4.7|🍛|GF|Chicken and Thai eggplant in a fragrant coconut green curry with basil.|chicken;green curry paste;coconut milk;thai eggplant;thai basil;fish sauce
Tom Yum Soup|Thai|Lunch,Dinner|30|4.6|🍲|GF|A hot and sour broth with shrimp, lemongrass, galangal and lime leaves.|shrimp;lemongrass;galangal;kaffir lime leaves;chilies;lime;fish sauce;mushrooms
Mango Sticky Rice|Thai|Dessert|40|4.8|🥭|VG,GF|Sweet coconut sticky rice with ripe mango slices.|glutinous rice;coconut milk;sugar;mango;sesame seeds
Som Tam|Thai|Lunch,Snack|20|4.5|🥗|GF|A crunchy, fiery green papaya salad pounded with lime and chilies.|green papaya;chilies;garlic;lime;fish sauce;palm sugar;peanuts;cherry tomatoes
Massaman Curry|Thai|Dinner|120|4.7|🥘|GF|A mild, rich curry with beef, potatoes and peanuts, scented with warm spices.|beef;massaman curry paste;coconut milk;potatoes;peanuts;tamarind
Thai Basil Chicken|Thai|Dinner,Lunch|20|4.6|🌿|GF|Minced chicken stir-fried with holy basil and chilies, with a fried egg on rice.|ground chicken;holy basil;chilies;garlic;oyster sauce;eggs;rice
Spring Rolls|Thai|Snack|40|4.4|🥢|VG|Crispy rolls filled with glass noodles and vegetables, with sweet chili sauce.|spring roll wrappers;glass noodles;cabbage;carrots;mushrooms;sweet chili sauce
Tofu Red Curry|Thai|Dinner|30|4.4|🍛|VG,GF|Golden tofu and vegetables in a spicy red coconut curry.|tofu;red curry paste;coconut milk;bell peppers;bamboo shoots;thai basil
Thai Iced Tea|Thai|Drink|10|4.5|🧋|V,GF|Strong spiced tea poured over ice with sweetened condensed milk.|thai tea;condensed milk;evaporated milk;sugar;ice
Kung Pao Chicken|Chinese|Dinner|25|4.6|🥜||Chicken stir-fried with peanuts, dried chilies and Sichuan pepper.|chicken;peanuts;dried chilies;sichuan peppercorns;soy sauce;black vinegar;scallions
Mapo Tofu|Chinese|Dinner|25|4.7|🌶️||Silky tofu in a numbing, spicy sauce with ground pork and doubanjiang.|silken tofu;ground pork;doubanjiang;sichuan peppercorns;garlic;scallions
Pork Dumplings|Chinese|Snack,Dinner|90|4.8|🥟||Juicy pork and chive dumplings, boiled and served with black vinegar.|flour;ground pork;chives;ginger;soy sauce;sesame oil;black vinegar
Egg Fried Rice|Chinese|Lunch,Dinner|15|4.4|🍳|V|Day-old rice tossed in a hot wok with egg, peas and scallions.|rice;eggs;peas;scallions;soy sauce;sesame oil
Char Siu|Chinese|Dinner|180|4.7|🍖||Cantonese barbecued pork with a sticky, honeyed glaze.|pork shoulder;hoisin sauce;honey;five spice;soy sauce;rice wine
Hot and Sour Soup|Chinese|Lunch|30|4.3|🍲||A peppery, tangy soup with tofu, mushrooms and ribbons of egg.|tofu;wood ear mushrooms;bamboo shoots;eggs;black vinegar;white pepper
Peking Duck Pancakes|Chinese|Dinner|240|4.8|🦆||Crisp-skinned duck with thin pancakes, cucumber, scallions and hoisin.|duck;maltose;pancakes;cucumber;scallions;hoisin sauce
Scallion Pancakes|Chinese|Snack,Breakfast|40|4.5|🥞|VG|Flaky, chewy flatbreads layered with scallions and fried golden.|flour;scallions;sesame oil;salt
Dan Dan Noodles|Chinese|Lunch,Dinner|25|4.6|🍜||Noodles with chili oil, sesame paste and crispy pork.|wheat noodles;ground pork;chili oil;sesame paste;sichuan peppercorns;bok choy
Egg Tarts|Chinese|Dessert,Breakfast|50|4.6|🥧|V|Flaky pastry cups holding a glossy, wobbly egg custard.|puff pastry;eggs;milk;sugar;evaporated milk
Steamed Bao Buns|Chinese|Snack,Lunch|120|4.5|🥯||Pillowy steamed buns with braised pork belly and pickles.|flour;yeast;pork belly;hoisin sauce;cucumber;cilantro;peanuts
Bubble Tea|Chinese|Drink|30|4.4|🧋|V,GF|Milk tea with chewy brown sugar tapioca pearls.|black tea;milk;tapioca pearls;brown sugar
Moussaka|Greek|Dinner|120|4.7|🍆|GF|Layers of eggplant and spiced lamb under a golden béchamel.|eggplant;ground lamb;tomatoes;cinnamon;onion;milk;butter;nutmeg
Greek Salad|Greek|Lunch|15|4.5|🥗|V,GF|Tomatoes, cucumber, olives and a slab of feta with oregano and olive oil.|tomatoes;cucumber;red onion;kalamata olives;feta;oregano;olive oil
Chicken Souvlaki|Greek|Dinner,Lunch|40|4.6|🍢|GF|Lemon and oregano chicken skewers with tzatziki and warm pita.|chicken;lemon;oregano;garlic;yogurt;cucumber;pita
Spanakopita|Greek|Lunch,Snack|75|4.5|🥬|V|Crisp phyllo filled with spinach, feta and dill.|phyllo;spinach;feta;eggs;dill;scallions;butter
Tzatziki|Greek|Snack|10|4.6|🥒|V,GF|Cool yogurt dip with cucumber, garlic and dill.|greek yogurt;cucumber;garlic;dill;lemon;olive oil
Baklava|Greek|Dessert|90|4.7|🍯|V|Layers of phyllo, walnuts and pistachios soaked in honey syrup.|phyllo;walnuts;pistachios;butter;honey;cinnamon
Gemista|Greek|Dinner|90|4.4|🫑|VG,GF|Tomatoes and peppers stuffed with herbed rice and baked until tender.|tomatoes;bell peppers;rice;onion;mint;parsley;olive oil
Avgolemono Soup|Greek|Lunch,Dinner|40|4.5|🍋|GF|A silky chicken soup thickened with egg and brightened with lemon.|chicken stock;chicken;rice;eggs;lemon;dill
Greek Yogurt with Honey|Greek|Breakfast,Dessert|5|4.4|🍯|V,GF|Thick yogurt with thyme honey and toasted walnuts.|greek yogurt;honey;walnuts
Grilled Octopus|Greek|Dinner|90|4.6|🐙|GF|Tender octopus charred on the grill with lemon, oregano and olive oil.|octopus;red wine vinegar;lemon;oregano;olive oil
Loukoumades|Greek|Dessert,Snack|45|4.5|🍩|V|Golden honey puffs sprinkled with cinnamon and walnuts.|flour;yeast;honey;cinnamon;walnuts
Lamb Kleftiko|Greek|Dinner|240|4.7|🍖|GF|Lamb slow-baked in parchment with garlic, lemon and potatoes.|lamb leg;garlic;lemon;oregano;potatoes;feta
Chicken Tagine with Lemon|Moroccan|Dinner|90|4.7|🍋|GF|Chicken slowly cooked with preserved lemons, green olives and saffron.|chicken;preserved lemons;green olives;saffron;ginger;onion;cilantro
Couscous with Vegetables|Moroccan|Dinner,Lunch|60|4.4|🥕|VG|Fluffy couscous under a stew of seven vegetables and chickpeas.|couscous;carrots;zucchini;turnips;chickpeas;pumpkin;ras el hanout
Harira|Moroccan|Dinner|90|4.6|🍲|VG|A warming tomato, lentil and chickpea soup with herbs and spices.|lentils;chickpeas;tomatoes;celery;cilantro;parsley;cinnamon;ginger
Lamb Tagine with Apricots|Moroccan|Dinner|150|4.8|🍑|GF|Sweet and savory lamb with apricots, honey and toasted almonds.|lamb shoulder;dried apricots;honey;almonds;cinnamon;ginger;onion
Zaalouk|Moroccan|Snack,Lunch|40|4.4|🍆|VG,GF|A smoky cooked eggplant and tomato salad with cumin and paprika.|eggplant;tomatoes;garlic;cumin;paprika;cilantro;olive oil
Shakshuka|Moroccan|Breakfast,Lunch|30|4.7|🍳|V,GF|Eggs poached in a spicy tomato and pepper sauce.|eggs;tomatoes;bell peppers;onion;cumin;paprika;harissa
Moroccan Mint Tea|Moroccan|Drink|10|4.6|🫖|VG,GF|Green tea with a fistful of fresh mint, poured from a height.|green tea;fresh mint;sugar
Msemen|Moroccan|Breakfast,Snack|60|4.4|🫓|VG|Square, flaky pan-fried flatbreads, delicious with honey.|flour;semolina;oil;salt
Kefta Tagine|Moroccan|Dinner|45|4.5|🧆|GF|Spiced meatballs simmered in tomato sauce with eggs cracked on top.|ground beef;cumin;paprika;tomatoes;eggs;parsley
Chebakia|Moroccan|Dessert|120|4.3|🍪|V|Sesame cookies folded into flowers, fried and dipped in honey.|flour;sesame seeds;anise;honey;orange blossom water
Classic Cheeseburger|American|Dinner,Lunch|25|4.6|🍔||A smashed beef patty with melted cheddar, pickles and special sauce.|ground beef;cheddar;burger buns;pickles;onion;mayonnaise;ketchup
Buttermilk Pancakes|American|Breakfast|25|4.7|🥞|V|Tall, fluffy pancakes with maple syrup and butter.|flour;buttermilk;eggs;butter;baking powder;maple syrup
Mac and Cheese|American|Dinner,Lunch|40|4.6|🧀|V|Elbow pasta in a sharp cheddar sauce with a crunchy breadcrumb top.|macaroni;cheddar;milk;butter;flour;breadcrumbs
Buffalo Wings|American|Snack|60|4.5|🍗|GF|Crispy wings tossed in hot sauce and butter, with blue cheese dip.|chicken wings;hot sauce;butter;blue cheese;celery
Clam Chowder|American|Lunch,Dinner|50|4.5|🥣|GF|Creamy New England soup with clams, potatoes and bacon.|clams;potatoes;bacon;onion;cream;thyme
Chocolate Chip Cookies|American|Dessert,Snack|30|4.8|🍪|V|Crisp edges, chewy middles and puddles of chocolate.|flour;butter;brown sugar;eggs;chocolate chips;vanilla
Pulled Pork Sandwich|American|Lunch,Dinner|480|4.7|🥪||Slow-smoked pork shoulder, pulled and piled high with coleslaw.|pork shoulder;barbecue rub;barbecue sauce;buns;cabbage
Apple Pie|American|Dessert|120|4.7|🥧|V|A flaky double crust around cinnamon-spiced apples.|apples;flour;butter;sugar;cinnamon;lemon
Cobb Salad|American|Lunch|25|4.3|🥗|GF|Rows of chicken, bacon, egg, avocado and blue cheese on crisp greens.|romaine;chicken;bacon;eggs;avocado;blue cheese;tomatoes
Blueberry Muffins|American|Breakfast,Snack|35|4.5|🧁|V|Tender muffins bursting with blueberries under a crumble top.|flour;blueberries;butter;sugar;eggs;milk
Avocado Toast|American|Breakfast|10|4.2|🥑|VG|Smashed avocado on sourdough with chili flakes and lemon.|sourdough;avocado;lemon;chili flakes;olive oil
Strawberry Milkshake|American|Drink,Dessert|5|4.4|🍓|V,GF|A thick shake of strawberries and vanilla ice cream.|strawberries;vanilla ice cream;milk
"""


def parse(line: str) -> dict:
    title, cuisine, meals, minutes, rating, emoji, diets, description, ingredients = line.split("|")
    diet_names = {"V": "Vegetarian", "VG": "Vegan", "GF": "Gluten-free"}
    diet_list = [diet_names[d] for d in diets.split(",") if d]
    if "Vegan" in diet_list and "Vegetarian" not in diet_list:
        diet_list.insert(0, "Vegetarian")
    return {
        "title": title,
        "cuisine": cuisine,
        "meal_types": meals.split(","),
        "total_time": int(minutes),
        "rating": float(rating),
        "emoji": emoji,
        "diets": diet_list,
        "description": description,
        "ingredients": ingredients.split(";"),
    }


def main() -> None:
    recipes = [parse(line) for line in RECIPES.strip().splitlines()]
    out = pathlib.Path(__file__).resolve().parent.parent / "web/modules/custom/meilisearch_demo/data/recipes.json"
    out.write_text(json.dumps(recipes, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {len(recipes)} recipes to {out}")


if __name__ == "__main__":
    main()
