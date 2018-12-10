from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User = User(name="Hadi Ramezani", email="hadi.ramezani@gmail.com", id=1,
            picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User)
session.commit()

# Items for Computers and Accessories
category = Category(id=1, name="Computers and Accessories", user_id=1)

session.add(category)
session.commit()

category_item = CategoryItem(user_id=1, name="Laptop",
                             description="A laptop, also called a notebook computer or simply a notebook, is a small, "
                                         "portable personal computer with a 'clamshell' form factor, having, typically,"
                                         " a thin LCD or LED computer screen mounted on the inside of the upper lid of "
                                         "the 'clamshell' and an alphanumeric keyboard on the inside of the lower lid. "
                                         "The 'clamshell' is opened up to use the computer. Laptops are folded shut for"
                                         " transportation, and thus are suitable for mobile use. Its name comes from "
                                         "'lap', as it was deemed to be placed for use on a person's lap. Although "
                                         "originally there was a distinction between laptops and notebooks, the former "
                                         "being bigger and heavier than the latter, as of 2014, there is often no "
                                         "longer any difference. Laptops are commonly used in a variety of settings, "
                                         "such as at work, in education, in playing games, Internet surfing, for "
                                         "personal multimedia and general home computer use.",
                             category=category)

session.add(category_item)
session.commit()


category_item = CategoryItem(user_id=1, name="Monitor",
                             description="A computer monitor is an output device that displays information in pictorial"
                                         " form. A monitor usually comprises the display device, circuitry, casing, and"
                                         " power supply. The display device in modern monitors is typically a thin film"
                                         " transistor liquid crystal display (TFT-LCD) with LED backlighting having "
                                         "replaced cold-cathode fluorescent lamp (CCFL) backlighting. Older monitors "
                                         "used a cathode ray tube (CRT). Monitors are connected to the computer via "
                                         "VGA, Digital Visual Interface (DVI), HDMI, DisplayPort, Thunderbolt, "
                                         "low-voltage differential signaling (LVDS) or other proprietary connectors "
                                         "and signals.",
                             category=category)

session.add(category_item)
session.commit()


category_item = CategoryItem(user_id=1, name="Networking Hardware",
                             description="Networking hardware, also known as network equipment or computer networking "
                                         "devices, are physical devices which are required for communication and "
                                         "interaction between devices on a computer network. Specifically, they "
                                         "mediate data in a computer network. Units which are the last receiver or "
                                         "generate data are called hosts or data terminal equipment.",
                             category=category)

session.add(category_item)
session.commit()


# Items for TV and Video
category = Category(id=2, name="TV and Video", user_id=1)

session.add(category)
session.commit()


category_item = CategoryItem(user_id=1, name="Television",
                             description="Television (TV), sometimes shortened to tele or telly is a telecommunication "
                                         "medium used for transmitting moving images in monochrome (black and white), "
                                         "or in colour, and in two or three dimensions and sound. The term can refer "
                                         "to a television set, a television program ('TV show'), or the medium of "
                                         "television transmission. Television is a mass medium for advertising, "
                                         "entertainment and news.",
                             category=category)

session.add(category_item)
session.commit()

category_item = CategoryItem(user_id=1, name="Projector",
                             description="A projector or image projector is an optical device that projects an image "
                                         "(or moving images) onto a surface, commonly a projection screen. Most "
                                         "projectors create an image by shining a light through a small transparent "
                                         "lens, but some newer types of projectors can project the image directly, by "
                                         "using lasers. A virtual retinal display, or retinal projector, is a "
                                         "projector that projects an image directly on the retina instead of using an "
                                         "external projection screen.",
                             category=category)

session.add(category_item)
session.commit()

category_item = CategoryItem(user_id=1, name="Home theater",
                             description="A home theater, a.k.a. home cinema, is a combination of audio and video "
                                         "components designed to recreate the experience of seeing movies in a theater",
                             category=category)

session.add(category_item)
session.commit()


# Items for Office Electronics
category = Category(id=3, name="Office Electronics", user_id=1)

session.add(category)
session.commit()

category_item = CategoryItem(user_id=1, name="Printer",
                             description="In computing, a printer is a peripheral device which makes a persistent "
                                         "human-readable representation of graphics or text on paper. The first "
                                         "computer printer designed was a mechanically driven apparatus by Charles "
                                         "Babbage for his difference engine in the 19th century; however, his "
                                         "mechanical printer design was not built until 2000.[2] The first electronic "
                                         "printer was the EP-101, invented by Japanese company Epson and released in "
                                         "1968. The first commercial printers generally used mechanisms from electric "
                                         "typewriters and Teletype machines. The demand for higher speed led to the "
                                         "development of new systems specifically for computer use. In the 1980s were "
                                         "daisy wheel systems similar to typewriters, line printers that produced "
                                         "similar output but at much higher speed, and dot matrix systems that could "
                                         "mix text and graphics but produced relatively low-quality output. The "
                                         "plotter was used for those requiring high quality line art like blueprints.",
                             category=category)

session.add(category_item)
session.commit()

category_item = CategoryItem(user_id=1, name="Calculator",
                             description="An electronic calculator is typically a portable electronic device used to "
                                         "perform calculations, ranging from basic arithmetic to complex mathematics. "
                                         "The first solid-state electronic calculator was created in the early 1960s. "
                                         "Pocket-sized devices became available in the 1970s, especially after the "
                                         "Intel 4004, the first microprocessor, was developed by Intel for the "
                                         "Japanese calculator company Busicom. They later became used commonly within "
                                         "the petroleum industry (oil and gas).",
                             category=category)

session.add(category_item)
session.commit()

print("added category items!")
