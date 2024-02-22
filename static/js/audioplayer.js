const PLAY_BUTTON_ICON_SVG = `<svg viewBox="0 0 11 15" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12.75 7.36122L-6.43538e-07 14.7224L0 1.36601e-06L12.75 7.36122Z" fill="black"/></svg>`;
const PAUSE_BUTTON_ICON_SVG = `<svg viewBox="0 0 9 15" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_8_3)"><path d="M3.28846 0H0V15H3.28846V0Z" fill="black"/><path d="M8.99999 0H5.71153V15H8.99999V0Z" fill="black"/></g><defs><clipPath id="clip0_8_3"><rect width="9" height="15" fill="white"/></clipPath></defs></svg>`;

class AudioPlayer extends HTMLElement {
  constructor() {
    super();
    this.audio = document.createElement("audio");
    this.audio.loop = true;

    this.attachShadow({ mode: "open" });
    this.shadowRoot.appendChild(this.audio);

    this.sheet = new CSSStyleSheet();
    this.sheet.replaceSync(`
    .music-player {
      display: grid;
      grid-template-columns: 72px 36px auto 36px 36px 36px;
      grid-template-rows: 36px 36px;
      background: var(--background);
      border: 2px solid var(--border-color);
      border-radius: 4px;
      column-gap: 8px;
      padding: 8px;
      color: var(--text-color);
      font-family: var(--font-family);
    }

    #play-pause-button {
      width: 100%;
      height: 100%;
      grid-column: 1 / 1;
      grid-row: 1 / 3;
      border-radius: 3px;
      background: var(--button-background);
      cursor: pointer;
      box-shadow: 0px 1px 1px var(--box-shadow-color-primary), 0px 0px 1px var(--box-shadow-color-secondary);
      border: 1px solid var(--border-color);
    }

    #play-pause-button svg {
      width: 38px;
      height: 38px;
      fill: var(--button-fill-color);
    }

    #current-time-label {
      font-size: 0.75rem;
      grid-column: 2 / 2;
      grid-row: 1 / 1;
      align-self: center;
    }

    #duration-label {
      font-family: monospace;
      font-size: 0.75rem;
      grid-column: 6 / 6;
      grid-row: 1 / 1;
      align-self: center;
    }

    #seeker-range {
      grid-column: 3 / 6;
      grid-row: 1 / 1;
    }

    #volume-range {
      grid-column: 4 / 7;
    }

    #track-name {
      grid-column: 2 / 4;
      grid-row: 2 / 2;
      align-self: center;
      font-size: 0.8rem;
      opacity: 0.75;
    }

    input[type=range] {
      -webkit-appearance: none;
      width: 100%; /* Specific width is required for Firefox. */
      background: transparent;
    }

    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      border: 1px solid var(--border-color);
      height: 16px;
      width: 16px;
      border-radius: 3px;
      background: var(--thumb-background);
      cursor: pointer;
      margin-top: -4px;
      box-shadow: 0px 1px 1px var(--box-shadow-color-primary), 0px 0px 1px var(--box-shadow-color-secondary);
    }
    input[type=range]::-moz-range-thumb {
      border: 1px solid var(--border-color);
      height: 16px;
      width: 16px;
      border-radius: 3px;
      background: var(--thumb-background);
      cursor: pointer;
      box-shadow: 0px 1px 1px var(--box-shadow-color-primary), 0px 0px 1px var(--box-shadow-color-secondary);
    }

    input[type=range]::-webkit-slider-runnable-track {
      width: 100%;
      height: 8.4px;
      cursor: pointer;
      border-radius: 1.3px;
      background: var(--slider-background);
      border: 0.2px solid bar(--border-color);
      box-shadow: 0px 1px 1px var(--box-shadow-color-primary), 0px 0px 1px var(--box-shadow-color-secondary);
    }

    input[type=range]:focus::-webkit-slider-runnable-track {
      background: var(--slider-background);
    }

    input[type=range]::-moz-range-track {
      width: 100%;
      height: 8.4px;
      cursor: pointer;
      background: var(--slider-background);
      border-radius: 1.3px;
      border: 0.2px solid black;
      box-shadow: 0px 1px 1px var(--box-shadow-color-primary), 0px 0px 1px var(--box-shadow-color-secondary);
    }
    `);

    this.shadowRoot.adoptedStyleSheets = [this.sheet];

    this._playOrPause = this._playOrPause.bind(this);

    this._playing = false;
    this._muted = false;
    this._src = "";
    this._type = "";
    this._filename = "";
    this._trackname = "";
    this._audioId = "";
    this._hoststyles = `
    :host {
      --background: white;
      --text-color: black;
      --border-color: black;
      --button-background: white;
      --button-fill-color: black;
      --slider-background: black;
      --thumb-background: white;
      --box-shadow-color-primary: black;
      --box-shadow-color-secondary: #0d0d0d;
      --font-family: monospace;
    }`;
  }

  set playing(isPlaying) {
    this._playing = isPlaying;
    if (isPlaying) {
      this.audio.play();
    } else {
      this.audio.pause();
    }
  }

  set muted(isMuted) {
    this._muted = isMuted;
    this.audio.muted = isMuted;
  }

  set src(newSrc) {
    this._src = newSrc;
  }

  set type(newType) {
    this._type = newType;
  }

  set filename(newFilename) {
    this._filename = newFilename;
  }

  set trackname(newTrackname) {
    this._trackname = newTrackname;
  }

  set audioId(newId) {
    this._audioId = newId;
  }

  set hostStyles(newStyles) {
    this._hoststyles = newStyles;
  }

  get playing() {
    return this._playing;
  }
  get muted() {
    return this._muted;
  }
  get src() {
    return this._src;
  }
  get type() {
    return this._type;
  }
  get filename() {
    return this._filename;
  }
  get trackname() {
    return this._trackname;
  }
  get audioId() {
    return this._audioId;
  }
  get hostStyles() {
    this.sheet.delete(0);
    this.sheet.insertRule(this._hoststyles, 0);
    return this._hoststyles;
  }

  _playOrPause() {
    this._playing = !this._playing;
    const button = this.shadowRoot.getElementById("play-pause-button");
    if (this.playing) {
      button.innerHTML = PAUSE_BUTTON_ICON_SVG;
      this.audio.play();
    } else {
      button.innerHTML = PLAY_BUTTON_ICON_SVG;
      this.audio.pause();
    }
  }

  static get observedAttributes() {
    return ["src", "type", "trackname", "filename", "audio-id", "host-style"];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    switch (name) {
      case "src":
        this._src = newValue;
        this.audio.src = newValue;
        break;
      case "type":
        this._type = newValue;
        this.audio.type = newValue;
        break;
      case "trackname":
        this._trackname = newValue;
        break;
      case "filename":
        this._filename = newValue;
        break;
      case "audio-id":
        this._audioId = newValue;
        break;
      case "host-style":
        this._hoststyles = newValue;

        break;
    }
  }

  connectedCallback() {
    const playerControls = document.createElement("div");
    playerControls.classList.add("music-player");
    playerControls.innerHTML = `
    <button id="play-pause-button">${PLAY_BUTTON_ICON_SVG}</button>
    <span id="current-time-label">00:00</span>
    <input id="seeker-range" type="range" min="0" max="100" value="0"/>
    <span id="duration-label">...</span>
    <span id="track-name">${this.trackname || this.filename}</span>
    <input id="volume-range" type="range" min="0" max="100" value="50"/>
    `;

    this.shadowRoot.appendChild(playerControls);

    const playPauseButton = this.shadowRoot.getElementById("play-pause-button");
    const seekerRange = this.shadowRoot.getElementById("seeker-range");
    const volumeRange = this.shadowRoot.getElementById("volume-range");
    const currentTimeLabel =
      this.shadowRoot.getElementById("current-time-label");
    const durationLabel = this.shadowRoot.getElementById("duration-label");
    playPauseButton.addEventListener("click", this._playOrPause);

    seekerRange.addEventListener("input", (event) => {
      this.audio.currentTime = event.target.value;
    });

    volumeRange.addEventListener("input", (event) => {
      const volume = event.target.value / 100;

      if (volume === 0) {
        this.muted = true;
      } else if (0 < volume && volume < 0.5) {
        this.muted = false;
      } else {
        this.muted = false;
      }

      this.audio.volume = volume;
    });

    this.audio.addEventListener("timeupdate", () => {
      const seconds = Math.floor(this.audio.currentTime);
      seekerRange.value = seconds;
      const min = Math.floor(seconds / 60);
      const sec = seconds % 60;
      const formattedMin = min < 10 ? `0${min}` : `${min}`;
      const formattedSec = sec < 10 ? `0${sec}` : `${sec}`;
      const label = `${formattedMin}:${formattedSec}`;
      currentTimeLabel.innerText = label;
    });

    this.audio.addEventListener("loadedmetadata", () => {
      const seconds = Math.floor(this.audio.duration);
      seekerRange.max = seconds;
      const min = Math.floor(seconds / 60);
      const sec = seconds % 60;
      const formattedMin = min < 10 ? `0${min}` : `${min}`;
      const formattedSec = sec < 10 ? `0${sec}` : `${sec}`;
      const label = `${formattedMin}:${formattedSec}`;
      durationLabel.innerText = label;
    });

    this.sheet.insertRule(this._hoststyles, 0);
  }

  disconnectedCallback() {}
}

customElements.define("audio-player", AudioPlayer);
