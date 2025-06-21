🛍️ AI-Powered E-commerce App with Product Recommendations and Semantic Search

This project is a full-stack e-commerce platform with integrated AI features for personalized product discovery. It combines:

✅ Django-based backend

✅ Stripe payment integration

✅ Machine Learning-powered recommender system

✅ Pinecone + Transformer embeddings for semantic product search

🚀 Features

🛒 E-Commerce Core

User registration, login, and session management

Product catalog with dynamic display

Add to cart, order history

Stripe-powered secure payment checkout

🧠 ML-Based Recommendation System

Collaborative filtering using Orders and Favourites tables

Weighted interaction matrix built per user

Cosine similarity to compute user-user similarity

Top product recommendations from similar users

🔍 Semantic Search via Pinecone

Transformer-based encoder to embed user prompts and product data

Vector similarity search using Pinecone's cloud index

Dynamic response to natural queries like:

"Find cheap black jackets under 100"

"Show red sneakers between 50 and 100"

📦 Project Components

/products/models.py

Contains models like Product, Orders, Favourites, CartItem, etc.

recommodation(request) view

Performs collaborative filtering:

Fetches all past user interactions

Combines orders and favourites with weights

Builds a user-product matrix

Computes cosine similarity

Recommends products based on similar users

Simple_Transformer

Custom Transformer decoder used to:

Tokenize and embed user queries

Generate 64-dim vectors via encode_text()

These vectors are then used in:

Pinecone upsert (product vectors)

Pinecone query (prompt vectors)

🔗 Tech Stack

Area - Tool

Backend - Django + PostgreSQL

Frontend - HTML, JS, Bootstrap

Payment Gateway - Stripe API

ML Framework - PyTorch

Vector Database - Pinecone

Semantic Search - Custom Transformer

🛠 Setup

Environment

Python 3.10+

Django 4+

PyTorch

Pinecone Python SDK

Quickstart

# Clone the repo
$ git clone your-repo-url
$ cd your-repo

# Install dependencies
$ pip install -r requirements.txt

# Setup Django
$ python manage.py migrate
$ python manage.py runserver

Screenshot
![Alt_text](https://github.com/anhadbatra/Ecommerce/blob/main/Screenshot%202025-06-20%20202327.png)


