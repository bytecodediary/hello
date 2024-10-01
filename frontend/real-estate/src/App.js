import Navbar from './Navbar';
import './App.css';
import Heroimg from './public/img/herohouse.png'

function App() {
  return (
    <div className="App">
      <Navbar/>
      <section className="container mx-auto px-4 py-12 flex items-center justify-between">
        <div className="flex px-4 items-center">
        <div className="hero-left flex-1">
          <h2 className="text-5xl font-bold leading-tight mb-4 text-black">Timberline Heights:Your getway platform for</h2>
          <p className="text-xl text-gray-600 mb-8 ">Timberline Heights is a userfriendly platform for property solutions, connecting customers and stakeholders</p>
          <div className="flex space-x-4" >
          <button className="bg-red-500 hover:bg-red-600 text-white px-4">
            Start Exploring
          </button>
          <button className="bg-white text-gray-800 border-gray-300 hover:bg-gray-100">
            Start Exploring
          </button>
          </div>
        </div>
         <div className="hero-right flex-1 ">
           <Image
            src={Heroimg} 
            alt="Colorful house illustration"
            width={400}
            height={400}
            className="object-contain"
           />
        </div> 
        </div>
      </section>
    </div>
  );
}

export default App;
