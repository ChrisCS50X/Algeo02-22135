import { useState } from 'react';

const InputImage = ({onSearch}:any) => {
    const [image, setImage] = useState('');
    const [isChecked, setIsChecked] = useState(false);
    const [error, setError] = useState('');
    
    const handleToggle = () => {
        setIsChecked(!isChecked);
    };

    const handleImageChange = (e: any) => {
        setImage(e.target.files[0]);
        setError(''); // Reset the error when a new image is selected
    };

    const searchHandler = async (e: any) => {
        e.preventDefault();

        // Check if the required fields are filled
        if (!image) {
        setError('Please select an image.');
        return;
        }

        try {
        // Perform your search or data processing here
        await onSearch({ isChecked, image });
        } catch (error) {
        console.error('Error during search:', error);
        setError('An error occurred during the search.');
        }
    };

    return (
        <>
            <form action="" onSubmit={searchHandler}>
                <div className="flex w-ful justify-between p-10 w-full">
                    <div className="flex justify-center items-center p-10 w-full">
                    {
                        image ? (
                            <div className="overflow-hidden bg-black rounded-lg shadow-md w-full h-80">
                                <img className="object-contain w-full h-full" src={URL.createObjectURL(image)} alt="Your Image"></img>
                            </div>
                        ) : (
                            <div className="overflow-hidden bg-[#d9d9d9] rounded-lg shadow-md w-full h-80"></div>
                        )
                    }
                    
                    </div>
                    <div className="flex justify-between items-center p-10 flex-col h-72">
                        <p className="text-blue-500 font-extrabold font-poppins">Image Input</p>
                        
                        <label className="bg-blue-500 hover:bg-blue-600 py-2 rounded-lg w-48 text-white mt-2 cursor-pointer text-center">
                            <input id="image-input" className="hidden" type="file" accept='image/*' onChange={handleImageChange}/>
                            Select Image
                        </label>
                        <div className="h-16"></div>
                        <div className="flex">
                            <span className="mr-3.5 font-poppins text-blue-500 font"> Color </span>
                            <div className="relative inline-block w-14 mr-2 align-middle select-none transition duration-200 ease-in">
                                <label htmlFor="toggle" className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer">
                                    <input type="checkbox" name="toggle" id="toggle" className="checked:bg-blue-500 bg-white toggle-checkbox absolute block w-6 h-6 rounded-full  border-4 appearance-none cursor-pointer" checked={isChecked} onChange={handleToggle}/>
                                </label>
                            </div>
                            <span className="ml-1 font-poppins text-blue-500"> Texture </span>
                        </div>
                        <button type='submit' className="transition-all duration-500 bg-size-200 bg-pos-0 hover:bg-pos-100 font-poppins font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 py-2 rounded-full text-white mt-2 w-48" >Search</button>
                    </div>
                </div>
                {error && <div className="text-red-500">{error}</div>}
            </form>
        </>
    )
}

export default InputImage