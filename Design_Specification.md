# Design Specification

## Introduction

This chapter focuses on the detailed design of the web application based on the requirements in the previous chapter. The architecture of the system and various UI created for each page will be explored and discussed here.

## Architecture

The client-server architecture is a common model used in web applications. The client side includes the user interface, while the server is responsible for processing requests. In the user interface, there are actions that the user can take to make a request to the server, such as navigating to different pages, logging in, registering, and searching.

Figure 4.1 shows the client-server architecture model used in this project.

![Figure 4.1 - Client-Server Architecture Model](Documentation/Design/Website%20Architecture.jpg)

Using Flask, the server-side rendering is used for this architecture. The server consists of files such as __init__.py, which defines the initialization code for the application, including the blueprints. All necessary logic is coded in the server-side. An Object-relational mapping (ORM) is utilized in the models.py file to create the schema of the database.

Using the client-side architecture with Flask provides a lightweight and flexible framework for building web applications. Additionally, this architecture can provide a balance between scalability and performance, as the server is necessary for providing the data and resources, while the client handles the display.

## Database Design

The main information this project needs to store are the user information and the product information. The Entity Relationship Diagram (ERD) below shows the four primary entities: User, Basket, Basket Item, and Product.

Their relationship to each other is as follows: there will only be one basket per user, and the basket will hold the information of the product. The relationship between the basket and product was many-to-many; however, data normalization was applied to reduce data redundancy and improve data integrity. The intermediate table basket_item stores the relationship between the two entities while keeping their data separate.

Figure 4.2 shows the Database ERD for this project.

![Figure 4.2 - Database ERD](documentation/Design/Database%20ERD.jpg)
