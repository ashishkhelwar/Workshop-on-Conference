/* ============================================================
   PRESENTATION AUDIO MANAGER
   – Slide transition whoosh
   – Optional forest ambient (wind + low drone)
   ============================================================ */

const AudioManager = (() => {
  let ctx = null;
  let ambientNodes = null;
  let muted = true;

  function getCtx() {
    if (!ctx) {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  /* Soft whoosh on slide change */
  function playTransition() {
    if (muted) return;
    try {
      const ac = getCtx();
      const osc  = ac.createOscillator();
      const gain = ac.createGain();
      osc.connect(gain);
      gain.connect(ac.destination);

      osc.type = 'sine';
      osc.frequency.setValueAtTime(700, ac.currentTime);
      osc.frequency.exponentialRampToValueAtTime(350, ac.currentTime + 0.18);
      gain.gain.setValueAtTime(0.07, ac.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.22);

      osc.start(ac.currentTime);
      osc.stop(ac.currentTime + 0.25);
    } catch (e) {}
  }

  /* Forest ambient: filtered wind noise + low drone */
  function startAmbient() {
    if (ambientNodes) return;
    try {
      const ac = getCtx();

      // Wind — looping white-noise buffer through low-pass filter
      const bufLen = ac.sampleRate * 4;
      const buf    = ac.createBuffer(1, bufLen, ac.sampleRate);
      const data   = buf.getChannelData(0);
      for (let i = 0; i < bufLen; i++) data[i] = Math.random() * 2 - 1;

      const noise = ac.createBufferSource();
      noise.buffer = buf;
      noise.loop   = true;

      const lpf = ac.createBiquadFilter();
      lpf.type            = 'lowpass';
      lpf.frequency.value = 500;
      lpf.Q.value         = 0.7;

      const windGain = ac.createGain();
      windGain.gain.value = 0.045;

      noise.connect(lpf);
      lpf.connect(windGain);
      windGain.connect(ac.destination);
      noise.start();

      // Low drone — sine oscillator for depth
      const drone     = ac.createOscillator();
      const droneGain = ac.createGain();
      drone.type            = 'sine';
      drone.frequency.value = 55;
      droneGain.gain.value  = 0.018;
      drone.connect(droneGain);
      droneGain.connect(ac.destination);
      drone.start();

      // Gentle second harmonic
      const drone2     = ac.createOscillator();
      const drone2Gain = ac.createGain();
      drone2.type            = 'sine';
      drone2.frequency.value = 110;
      drone2Gain.gain.value  = 0.008;
      drone2.connect(drone2Gain);
      drone2Gain.connect(ac.destination);
      drone2.start();

      ambientNodes = { noise, drone, drone2, windGain, droneGain, drone2Gain };
    } catch (e) {}
  }

  function stopAmbient() {
    if (!ambientNodes) return;
    try { ambientNodes.noise.stop();  } catch (e) {}
    try { ambientNodes.drone.stop();  } catch (e) {}
    try { ambientNodes.drone2.stop(); } catch (e) {}
    ambientNodes = null;
  }

  /* Toggle mute — returns true when sound is ON */
  function toggle() {
    muted = !muted;
    if (!muted) {
      startAmbient();
    } else {
      stopAmbient();
    }
    updateBtn();
    return !muted;
  }

  function updateBtn() {
    const btn = document.getElementById('soundBtn');
    if (!btn) return;
    btn.textContent = muted ? '🔇' : '🔊';
    btn.title       = muted ? 'Enable sound' : 'Mute sound';
  }

  return { playTransition, toggle };
})();
