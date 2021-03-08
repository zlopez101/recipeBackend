def Recipes() -> list:
    """Returns the list of 3 test recipes

    :return: list of recipes. Recipes are dictionaries
    :rtype: list
    """
    return [
        {
            "name": "25 Minute Korean Bulgogi BBQ Chicken with Spicy Garlic Butter Corn. ",
            "source": "Half Baked Harvest",
            "ingredients": [
                "1 pound boneless skinless chicken thighs or breasts  thinly sliced ",
                "2 tablespoons corn starch or flour ",
                "3 tablespoons sesame oil or extra virgin olive oil ",
                "1/2 cup low sodium soy sauce ",
                "3-4 tablespoons Gochujang  (Korean chili paste) ",
                "1 tablespoon ketchup ",
                "1 inch fresh ginger  grated ",
                "4-5 cloves garlic  minced or grated ",
                "3 green onions  chopped  plus more for serving ",
                "3 tablespoons salted butter ",
                "4 ears corn  kernels  removed from cob ",
                "2 medium shallots  sliced or chopped ",
                "1 jalapeño  seeded (if desired) and chopped ",
                "1/4 cup fresh cilantro  roughly chopped ",
                "3 cups steamed white or brown rice ",
                "yum yum sauce and sesame seeds  for serving ",
            ],
            "url": "https://www.halfbakedharvest.com/korean-bulgogi-bbq-chicken/",
        },
        {
            "name": "Super Simple Coconut Chicken Tikka Masala. ",
            "source": "Half Baked Harvest",
            "ingredients": [
                "1 medium yellow onion  quartered ",
                "1 shallot  halved ",
                "6 cloves garlic ",
                "2 (1-inch) pieces fresh ginger  peeled ",
                "3 tablespoons garam masala ",
                "2 teaspoons ground turmeric ",
                "2 teaspoons kosher salt ",
                "1 teaspoon crushed red pepper flakes ",
                "Zest of 1 lemon ",
                "2 pounds boneless skinless chicken breast  cubed ",
                "1⁄2 cup full-fat plain Greek yogurt ",
                "1 can (14 ounce) full-fat unsweetened coconut milk ",
                "1 can (6 ounce) tomato paste ",
                "1⁄4 cup cilantro  chopped ",
                "3 cups cooked rice  for serving ",
            ],
            "url": "https://www.halfbakedharvest.com/chicken-tikka-masala/",
        },
        {
            "name": "Queso Fundido Taquitos. ",
            "source": "Half Baked Harvest",
            "ingredients": [
                "1/2 pound ground Mexican chorizo (optional) ",
                "1 yellow onion  chopped ",
                "1 cup shredded sharp cheddar cheese ",
                "1 cup Monterey Jack cheese  cubed ",
                "1/2 cup shredded mozzarella cheese ",
                "1 poblano  seeded  and finely chopped ",
                "1 chipotle chile in adobo  finely chopped ",
                "16-20 corn tortillas  warmed ",
                "yogurt  cilantro  salsa  shredded lettuce  and pickled onions  for serving ",
                "2 avocados  halved ",
                "1/2 cup fresh cilantro ",
                "1 clove garlic  grated  ",
                "juice from 2 limes ",
                "flaky salt ",
            ],
            "url": "https://www.halfbakedharvest.com/queso-fundido-taquitos/",
        },
    ]


def Users() -> list:
    """Returns the list of 2 test users

    :return: list of users. Users are dictionaries
    :rtype: list
    """
    return [
        {
            "fname": "Jim",
            "lname": "Bob",
            "phone_number": "+11234567890",
            "email": "JimBob@gmail.com",
            "password": "JimIsCool",
        },
        {
            "fname": "Kim",
            "lname": "Sue",
            "phone_number": "+098754321",
            "email": "KimSue@gmail.com",
            "password": "KimIsCool",
        },
    ]
