import "./App.css";
import BackgroundVideo from "./components/BackgroundVideo";
import sonIcon from "./assets/son.png";
import sound from "./assets/minecraft_cat_sound.mp3";

function App() {
  return (
    <>
      <BackgroundVideo />
      <div className="app-container">
        <div className="sound_logo">
          <audio src={sound} autoPlay />
          <img src={sonIcon} />
        </div>
        <div className="searchbar">
          <input type="text" placeholder="Recherchez un jeu..."></input>
        </div>
      </div>
    </>
  );
}

export default App;
