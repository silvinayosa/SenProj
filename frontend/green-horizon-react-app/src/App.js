
import Header from "./components/Header";
import Home from "./components/Home";
import Footer from "./components/Footer";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SearchPage from "./components/SearchPage";

const App =()=> (
  <div className="app">
    <Router>
      <Header />

      <Routes>
          <Route path="/search" element={<SearchPage />} />
          <Route path="/" element={<Home />} />
      </Routes>
  
      <Footer />
    </Router>
  </div>
)

export default App;