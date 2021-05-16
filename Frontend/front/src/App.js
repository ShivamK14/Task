import React, { useState } from "react";
import axios from "axios";
import DateRangePicker from '@wojtekmaj/react-daterange-picker';

function MyApp() {
  const [value, onChange] = useState([new Date(), new Date()]);
  const [link ,setLink]= useState('/')
  return (
    <div>
      <DateRangePicker
        onChange={onChange}
        value={value}
      />
      <button onClick={(e) => {
        console.log(value);
        axios({
          // Endpoint to send files
          url: "http://127.0.0.1:8000/api/getdate/",
          method: "POST",
          // Attaching the form data
          data: {
            'start_date': value[0],
            'end_date': value[1]
          },
        })
          .then((res) => {
            console.log(res.data)
            setLink(res.data) 
            link.click()
          }) // Handle the response from backend here
          .catch((err) => { });
      }}>
        Generate
      </button>
      <br />
      <br />
      <a href={link} style={{ cursor: 'pointer' }}>Download</a>
    </div>
  );
}

class App extends React.Component {
  
  constructor(props) {
    super(props)
    this.state = {
      html: null
    }
  }

  handleImageChange = (e) => {
    this.setState({
      image: e.target.files[0]
    })
  };
  handlexmlChange = (e) => {
    this.setState({
      xml: e.target.files[0]
    })
  };
  handleUpload(e) {

    let formData = new FormData();
    formData.append('image', this.state.image, this.state.image.name);
    formData.append('xml', this.state.xml, this.state.xml.name);

    axios({
      // Endpoint to send files
      url: "http://127.0.0.1:8000/api/image/",
      method: "POST",
      data: formData,
    })
      .then((response) => {
        const data = response.data;
        this.setState({html:data})
        console.log(response.data)
      }
      )

      .catch((err) => { }); // Catch errors if any
  }

  render() {
    return (
      <div>
                    <h1>Select your files</h1>
                    <h2>
                      Add Image
                    </h2>
                    <input
                      type="file"
                      id="image"  //To select multiple files
                      accept="image/png, image/jpeg"
                      onChange={(e) => this.handleImageChange(e)}
                    />
                    <h2>
                      Add XML
                    </h2>
                    <input
                      type="file"
                      id="data"  //To select multiple files
                      accept="data/xml"
                      onChange={(e) => this.handlexmlChange(e)}
                      />
                      <button onClick={(e) => this.handleUpload(e)}>Detect Object</button>
        <img src={this.state.html} style={{ cursor: 'pointer' }}></img>
        <br />
        <br />
        <h1>
          Generate CSV
        </h1>
        <div>
          <MyApp/>
        </div>
        </div>
    );
  }
}

export default App;