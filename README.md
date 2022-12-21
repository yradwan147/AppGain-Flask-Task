## AppGain URL Shortener
Basic API to handle a URL shortener app. Backend is built using Flask and PyMongo and connected to MongoDB Atlas. Frontend is built using React which is backed up with Vite for easier and faster development

The 3 main requests present in the backend and frontend are as follows
- List all existing URLs
- Add a new URL to shorten
- Update an existing URL

These 3 functionalities are available as endpoints in the backend which are called from the frontend.

#### List
A GET request endpoint that returns all existing mongoDB documents in a list for preview.

#### Add
A POST request endpoint that recieves JSON data format including all required arguments (i.e. web, ios, android and/or slug) and uses this data to create a new document in the database.

#### Update
A PUT request endpoint that recieves JSON data format including the targeted attributes to update and updates the targeted document accordingly based on the slug provided in the URL as an argument.


### Database Schema

```{
    slug: "s5G1f3"
    ios:
        primary: "http://..."
        fallback: "http://..."
    android:
        primary: "http://..."
        fallback: "http://..."
    web: "http://..."
}
```

To run the backend, download the needed dependencies from requirements.txt, and run "python app.py". (Used Python is 3.8.10)
To run the frontend, download node modules in the frontend folder and run "npm run dev" to run a development build.
