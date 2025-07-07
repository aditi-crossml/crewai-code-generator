```bash
# 1. Create the project directory
mkdir ecommerce-crud-app
cd ecommerce-crud-app

# 2. Initialize the backend (Node.js)
mkdir backend
cd backend
npm init -y  # Initialize a default package.json file

# 3. Install backend dependencies
npm install express mongoose cors dotenv bcrypt jsonwebtoken

#   - express:  For creating the server and handling routes.
#   - mongoose: For interacting with MongoDB.
#   - cors:     For handling Cross-Origin Resource Sharing (CORS) to allow frontend requests.
#   - dotenv:   For managing environment variables.
#   - bcrypt:   For password hashing.
#   - jsonwebtoken: For authentication and authorization.

# 4. Create backend file structure (example)
mkdir models routes controllers middleware
touch server.js models/Product.js routes/productRoutes.js controllers/productController.js middleware/authMiddleware.js

# 5. Example backend server.js (basic setup - adjust as needed)
cat > server.js <<EOL
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');

const productRoutes = require('./routes/productRoutes');

dotenv.config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json()); // For parsing application/json
app.use(express.urlencoded({ extended: true })); // For parsing application/x-www-form-urlencoded

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/ecommerce', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

// Routes
app.use('/api/products', productRoutes);

app.get('/', (req, res) => {
  res.send('E-commerce CRUD App Backend');
});

app.listen(port, () => {
  console.log(\`Server is running on port \${port}\`);
});

EOL

# Example .env file setup
cat > .env <<EOL
PORT=5000
MONGODB_URI=mongodb://localhost:27017/ecommerce  # Replace with your MongoDB URI
JWT_SECRET=your-secret-key  # Replace with a strong, random secret key
EOL

# 5.1 Example backend model (models/Product.js)
cat > models/Product.js <<EOL
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String, required: true },
  price: { type: Number, required: true },
  imageUrl: { type: String },
}, {
  timestamps: true
});

module.exports = mongoose.model('Product', productSchema);
EOL

# 5.2 Example backend controller (controllers/ProductController.js)
cat > controllers/productController.js <<EOL
const Product = require('../models/Product');

// Create a new product
exports.createProduct = async (req, res) => {
  try {
    const product = new Product(req.body);
    const savedProduct = await product.save();
    res.status(201).json(savedProduct);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

// Get all products
exports.getAllProducts = async (req, res) => {
  try {
    const products = await Product.find();
    res.json(products);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

// Get a single product by ID
exports.getProductById = async (req, res) => {
  try {
    const product = await Product.findById(req.params.id);
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json(product);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

// Update a product
exports.updateProduct = async (req, res) => {
  try {
    const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json(product);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

// Delete a product
exports.deleteProduct = async (req, res) => {
  try {
    const product = await Product.findByIdAndDelete(req.params.id);
    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json({ message: 'Product deleted' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
EOL

# 5.3 Example backend route (routes/productRoutes.js)
cat > routes/productRoutes.js <<EOL
const express = require('express');
const router = express.Router();
const productController = require('../controllers/productController');

// Create a new product
router.post('/', productController.createProduct);

// Get all products
router.get('/', productController.getAllProducts);

// Get a single product by ID
router.get('/:id', productController.getProductById);

// Update a product
router.put('/:id', productController.updateProduct);

// Delete a product
router.delete('/:id', productController.deleteProduct);

module.exports = router;
EOL


# 6. Go to the frontend directory
cd ..
mkdir frontend
cd frontend

# 7. Create a new React app
npx create-react-app .  # Creates a React app in the current directory.  ('.');

# 8. Install frontend dependencies
npm install axios react-router-dom redux react-redux redux-thunk

#   - axios:           For making HTTP requests to the backend.
#   - react-router-dom: For handling routing within the React app.
#   - redux:            For state management.
#   - react-redux:      For connecting React components to the Redux store.
#   - redux-thunk:      For handling asynchronous actions in Redux.

# 9.  Create frontend file structure (example)
mkdir src/components src/pages src/redux src/actions src/reducers
touch src/components/ProductCard.js src/pages/ProductList.js src/pages/ProductDetails.js src/pages/AddProduct.js src/pages/EditProduct.js src/redux/store.js src/actions/productActions.js src/reducers/productReducer.js

# 10. Example React component (src/components/ProductCard.js - adjust as needed)
cat > src/components/ProductCard.js <<EOL
import React from 'react';

const ProductCard = ({ product }) => {
  return (
    <div>
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <p>Price: \${product.price}</p>
    </div>
  );
};

export default ProductCard;
EOL

# Example React App.js (src/App.js - adjust as needed)
cat > src/App.js <<EOL
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProductList from './pages/ProductList';
import ProductDetails from './pages/ProductDetails';
import AddProduct from './pages/AddProduct';
import EditProduct from './pages/EditProduct';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>E-commerce CRUD App</h1>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/products/:id" element={<ProductDetails />} />
          <Route path="/add" element={<AddProduct />} />
          <Route path="/edit/:id" element={<EditProduct />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
EOL

# 10.1 Example React Action (src/actions/productActions.js)
cat > src/actions/productActions.js <<EOL
import axios from 'axios';

export const fetchProducts = () => {
  return async (dispatch) => {
    try {
      const response = await axios.get('/api/products');
      dispatch({ type: 'FETCH_PRODUCTS_SUCCESS', payload: response.data });
    } catch (error) {
      dispatch({ type: 'FETCH_PRODUCTS_FAILURE', payload: error.message });
    }
  };
};

export const addProduct = (product) => {
    return async (dispatch) => {
        try {
            const response = await axios.post('/api/products', product);
            dispatch({ type: 'ADD_PRODUCT_SUCCESS', payload: response.data });
        } catch (error) {
            dispatch({ type: 'ADD_PRODUCT_FAILURE', payload: error.message });
        }
    };
};

export const deleteProduct = (id) => {
    return async (dispatch) => {
        try {
            await axios.delete(\`/api/products/\${id}\`);
            dispatch({ type: 'DELETE_PRODUCT_SUCCESS', payload: id });
        } catch (error) {
            dispatch({ type: 'DELETE_PRODUCT_FAILURE', payload: error.message });
        }
    };
};

export const updateProduct = (id, product) => {
    return async (dispatch) => {
        try {
            const response = await axios.put(\`/api/products/\${id}\`, product);
            dispatch({ type: 'UPDATE_PRODUCT_SUCCESS', payload: response.data });
        } catch (error) {
            dispatch({ type: 'UPDATE_PRODUCT_FAILURE', payload: error.message });
        }
    };
};

export const getProduct = (id) => {
    return async (dispatch) => {
        try {
            const response = await axios.get(\`/api/products/\${id}\`);
            dispatch({ type: 'GET_PRODUCT_SUCCESS', payload: response.data });
        } catch (error) {
            dispatch({ type: 'GET_PRODUCT_FAILURE', payload: error.message });
        }
    };
};
EOL

# 10.2 Example React Reducer (src/reducers/productReducer.js)
cat > src/reducers/productReducer.js <<EOL
const initialState = {
  products: [],
  product: null,
  loading: false,
  error: null,
};

const productReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'FETCH_PRODUCTS_SUCCESS':
      return { ...state, products: action.payload, loading: false, error: null };
    case 'FETCH_PRODUCTS_FAILURE':
      return { ...state, loading: false, error: action.payload };
    case 'ADD_PRODUCT_SUCCESS':
      return {
        ...state,
        products: [...state.products, action.payload],
        loading: false,
        error: null,
      };
    case 'ADD_PRODUCT_FAILURE':
      return { ...state, loading: false, error: action.payload };
    case 'DELETE_PRODUCT_SUCCESS':
      return {
        ...state,
        products: state.products.filter((product) => product._id !== action.payload),
        loading: false,
        error: null,
      };
    case 'DELETE_PRODUCT_FAILURE':
      return { ...state, loading: false, error: action.payload };
    case 'UPDATE_PRODUCT_SUCCESS':
        return {
            ...state,
            products: state.products.map(product =>
                product._id === action.payload._id ? action.payload : product
            ),
            loading: false,
            error: null,
        };
    case 'UPDATE_PRODUCT_FAILURE':
        return { ...state, loading: false, error: action.payload };
    case 'GET_PRODUCT_SUCCESS':
        return { ...state, product: action.payload, loading: false, error: null };
    case 'GET_PRODUCT_FAILURE':
        return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
};

export default productReducer;
EOL

# 10.3 Example React Store (src/redux/store.js)
cat > src/redux/store.js <<EOL
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import { composeWithDevTools } from 'redux-devtools-extension';
import productReducer from './reducers/productReducer';

const store = createStore(
  productReducer,
  composeWithDevTools(applyMiddleware(thunk))
);

export default store;
EOL

# 10.4 Example React ProductList Page (src/pages/ProductList.js)
cat > src/pages/ProductList.js <<EOL
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchProducts, deleteProduct } from '../actions/productActions';
import ProductCard from '../components/ProductCard';
import { Link } from 'react-router-dom';

const ProductList = () => {
  const dispatch = useDispatch();
  const { products, loading, error } = useSelector((state) => state);

  useEffect(() => {
    dispatch(fetchProducts());
  }, [dispatch]);

  const handleDelete = (id) => {
    dispatch(deleteProduct(id));
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div>
      <h2>Product List</h2>
      <Link to="/add">Add New Product</Link>
      {products.map((product) => (
        <div key={product._id}>
          <ProductCard product={product} />
          <Link to={\`/edit/\${product._id}\`}>Edit</Link>
          <button onClick={() => handleDelete(product._id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
EOL

# 10.5 Example React ProductDetails Page (src/pages/ProductDetails.js)
cat > src/pages/ProductDetails.js <<EOL
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getProduct } from '../actions/productActions';

const ProductDetails = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { product, loading, error } = useSelector((state) => state);

  useEffect(() => {
    dispatch(getProduct(id));
  }, [dispatch, id]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  if (!product) {
    return <p>Product not found</p>;
  }

  return (
    <div>
      <h2>Product Details</h2>
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <p>Price: \${product.price}</p>
    </div>
  );
};

export default ProductDetails;
EOL

# 10.6 Example React AddProduct Page (src/pages/AddProduct.js)
cat > src/pages/AddProduct.js <<EOL
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { addProduct } from '../actions/productActions';
import { useNavigate } from 'react-router-dom';

const AddProduct = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const newProduct = {
      name,
      description,
      price: parseFloat(price),
    };
    dispatch(addProduct(newProduct));
    navigate('/');
  };

  return (
    <div>
      <h2>Add Product</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description:</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Price:</label>
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </div>
        <button type="submit">Add Product</button>
      </form>
    </div>
  );
};

export default AddProduct;
EOL

# 10.7 Example React EditProduct Page (src/pages/EditProduct.js)
cat > src/pages/EditProduct.js <<EOL
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import { getProduct, updateProduct } from '../actions/productActions';

const EditProduct = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { product } = useSelector((state) => state);

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');

  useEffect(() => {
    dispatch(getProduct(id));
  }, [dispatch, id]);

  useEffect(() => {
    if (product) {
      setName(product.name);
      setDescription(product.description);
      setPrice(product.price);
    }
  }, [product]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const updatedProduct = {
      name,
      description,
      price: parseFloat(price),
    };
    dispatch(updateProduct(id, updatedProduct));
    navigate('/');
  };

  return (
    <div>
      <h2>Edit Product</h2>
      {product ? (
        <form onSubmit={handleSubmit}>
          <div>
            <label>Name:</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Description:</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Price:</label>
            <input
              type="number"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
            />
          </div>
          <button type="submit">Update Product</button>
        </form>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default EditProduct;
EOL


# 11.  Optional: Initialize a Git repository
cd ..
git init
git add .
git commit -m "Initial commit"

# Summary of the setup:
# - Created project structure with 'backend' and 'frontend' directories.
# - Initialized Node.js backend with necessary dependencies (Express, Mongoose, CORS, Dotenv, Bcrypt, JWT).
# - Created a basic 'server.js' file and example folder structure for models, routes, controllers, and middleware in the backend.
# - Created a React frontend using create-react-app and installed Axios, React Router, Redux, React-Redux and Redux-Thunk.
# - Created a basic example component and a basic folder structure for components, pages, redux actions and reducers in the frontend.
# - Optionally initialized a Git repository.

# Next Steps:
# 1. Implement the backend API endpoints (CRUD operations for products).
# 2. Implement the frontend components and pages to interact with the backend API.
# 3. Set up Redux store and actions to manage application state.
# 4. Add styling and improve the user interface.
# 5. Implement authentication and authorization.
```