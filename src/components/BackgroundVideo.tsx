import myVideo from "../assets/minecraft_loop.mp4";

function BackgroundVideo() {
  return (
    <div>
      <video src={myVideo} autoPlay muted loop></video>
    </div>
  );
}

export default BackgroundVideo;
