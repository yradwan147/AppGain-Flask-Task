import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";
import { useForm } from "react-hook-form";
import axios from 'axios';
import { Add } from "./Add";
import { Update } from "./Update";

function App() {

  // React Form for ease of implementation
  const { register, handleSubmit } = useForm();

  // Documents state to update page when they are updated
  const [docs, setDocs] = useState([])


  // Renders document list to table
  const TableRenderer = ()=>{
    if (docs == []){
      return <></>
    }

    return <>
            {docs.map((value,id)=>{
              return <tr key={id}>
                      <td>{value.slug}</td>
                      <td>{value.ios.primary}</td>
                      <td>{value.ios.fallback}</td>
                      <td>{value.android.primary}</td>
                      <td>{value.android.fallback}</td>
                      <td>{value.web}</td>
                    </tr>
            })}
          </>
  }

  // Gets Document List
  const fetchData = async () =>{
    try {
      const {data: response} = await axios.get('http://127.0.0.1:8000/shortlinks');
      setDocs(response);
    } catch (error) {
      console.error(error.message);
    }
  }

  // Runs the "get document list" function once the page starts in the background
  useEffect(() => {
    fetchData();
    return () => {
    }
  }, [])
  

  return (
    <div>
      <Add/>
      <br/>
      <Update/>
      <br/>

      <table className="table">
        <thead className="thead-dark">
          <tr>
            <th>Slug</th>
            <th>IOS Primary</th>
            <th>IOS Fallback</th>
            <th>Android Primary</th>
            <th>Android Fallback</th>
            <th>Web</th>
          </tr>
        </thead>
        <tbody>
        
        <TableRenderer/>
        </tbody>
      </table>
    </div>
  );
}

export default App;
