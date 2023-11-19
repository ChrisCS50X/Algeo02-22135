"use client"
import React, { useState } from 'react';
import Link from 'next/link';
import { time } from 'console';
import Pagination from '@mui/material/Pagination';


const ImageGallery = ({ resultData,resultTime } : any) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [imagesPerPage] = useState(6);
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  

  const handleImageClick = async (image:any) => {
    try {
      const module = await import(`../../backend/upload_images/${image.nama_file}`);
      setSelectedImage(module.default);
    } catch (error) {
      console.error('Error loading image:', error);
    }
  };
  const handleFileChange = async(e:any) => {
    console.log("masuk satu");
    const folder = e.target.files[0];
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/hapusdataset/', {
        method: 'POST',
        body: "tes",
      });

      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }

    for (let i = 0; i < e.target.files.length; i++) {
      const file = e.target.files[i];
      const formData = new FormData();
      formData.append('file', file);
      console.log("masuk 2");
      try {
        const response = await fetch('http://127.0.0.1:8000/upload/', {
          method: 'POST',
          body: formData,
        });
  
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
    
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/uploadtodatabase/', {
        method: 'POST',
        body: "tes",
      });

      const data = await response.json();
      console.log(data);
      setLoading(false);
    } catch (error) {
      console.error('Error uploading file:', error);
      setLoading(false);
    }
  };

  
  // Change page
  const [page, setPage] = React.useState(1);
  const handleChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };
  // Get current images
  const indexOfLastImage = page * imagesPerPage;
  const indexOfFirstImage = indexOfLastImage - imagesPerPage;
  const currentData = resultData.slice(indexOfFirstImage, indexOfLastImage);



  return (
    <div>
      <div className='flex justify-between my-5'>
        <p className="text-blue-500 font-extrabold font-poppins">Result</p>
        <p className="font-poppins">{resultData.length} results in {resultTime.toFixed(2)} seconds</p>
      </div>
      {loading ? (
        // Display a loading spinner or message
        <div className='justify-center'>Loading...</div>
      ) : (
        // Your regular content goes here
        <>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4">
        {currentData.map((data : any, index : any) => (
        <figure key={index} className="w-full relative rounded-md drop-shadow-lg flex justify-center">
          <img src={`data:image/jpeg;base64,${data.images}`} alt={"image"} className="object-cover h-48 w-full" />
          <figcaption className="absolute bottom-0 z-90 w-3/4  px-5 py-2 text-white text-center text-sh ">
            <span className="text-l font-extrabold" style={{ textShadow: '0 0 5px black' }}>{data.persentase.toFixed(2)}%</span>
          </figcaption>
        </figure>
        ))}
      </div>
      <br></br>
      <div className='flex justify-center'>
      <Pagination count={Math.ceil(resultData.length/6)} page={page} shape="rounded" onChange={handleChange} /></div>
      <br></br>
      <hr className="w-full h-1 bg-[#d9d9d9]"></hr>
      <form action="">
        <div className="flex justify-center mb-10">
            <label className="transition-all duration-500 bg-size-200 bg-pos-0 hover:bg-pos-100 font-extrabold font-poppins bg-gradient-to-r from-blue-600 to-purple-600 py-2 rounded-lg w-48 text-white mt-2 cursor-pointer text-center">
                <input id="image-input" className="hidden" type="file" onChange={handleFileChange} directory="" webkitdirectory="" mozdirectory=""/>
                Upload Folder
            </label>
        </div>
      </form>
      </>
      )}
      
    </div>
  );
};



export default ImageGallery;
