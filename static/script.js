const txText = document.getElementById("tx-text")
const txBtn = document.getElementById("tx-btn")
// const txLed = document.getElementById("tx-led")
const txOutput = document.getElementById("tx-output")
const txAudio = document.getElementById("tx-audio")
const txDownload = document.getElementById("tx-download")



txBtn.addEventListener('click', async() => {
    const text = txText.value.trim()
    if(!text) {
        alert("provide some text dawg")
        return
    }

    txBtn.disabled = true

    try {
        const res = await fetch("/encode", {
            method: "POST",
            headers: {
                'Content-Type': "application/json"
            },
            body: JSON.stringify({ text })
        })

        if(!res.ok) {
            const err = await res.json().catch(() => ({error: "encode failed"}))
            throw new Error(err.error || "encode failed")
        }

        const blob = await res.blob()
        const url = URL.createObjectURL(blob)
        txAudio.src = url
        txDownload.href = url
        txOutput.classList.remove("hidden")
    } catch (error) {
        alert("encoding failed lmao: " + error.message)
    } finally {
        txBtn.disabled = false
    }
})




const rxFile = document.getElementById("rx-file")
const rxBtn = document.getElementById("rx-btn")
// const rxLed = document.getElementById("rx-led")
const rxReadout = document.getElementById("rx-readout")
const rxRecordBtn = document.getElementById("rx-record-btn")
const rxRecordStatus = document.getElementById("rx-record-status")

const READOUT_BASE = "font-mono text-sm bg-bg border border-borderLight rounded p-3 min-h-[44px] whitespace-pre-wrap break-words"

let pendingBlob = null

rxFile.addEventListener("change", () => {
    pendingBlob = rxFile.files[0] || null;
})

const decodeBlob = async(blob) => {
    rxBtn.disabled = true
    rxReadout.className = `${READOUT_BASE} text-textDim`
    rxReadout.textContent = 'decoding...'

    const formData = new FormData()
    formData.append('audio', blob, "audio.wav")

    try {
        const res = await fetch("/decode", {
            method: "POST",
            body: formData
        })
        const data = await res.json()

        if(!res.ok) {
            if(data.checksum_failed) {
                rxReadout.className = `${READOUT_BASE} text-amber`
                rxReadout.textContent = `⚠️ checksum mismatch: received (corrupted):\n"${data.partial_text}\nerror: ${data.error}"`
                return
            }

            throw new Error(data.error || "decode failed");
        }

        rxReadout.className = `${READOUT_BASE} text-green`
        rxReadout.textContent = data.text
    } catch (error) {
        rxReadout.className = `${READOUT_BASE} text-red`
        rxReadout.textContent = error.message
    } finally {
        rxBtn.disabled = false;
    }
}

rxBtn.addEventListener('click', async() => {
    if(!pendingBlob) {
        alert("no waveform or recording was provided :(")
        return
    }

    decodeBlob(pendingBlob)
})


// RECORDING 




let recorder = null
let micStream = null
let isRecording = false

const MAX_RECORD_MS = 60000
let recordTimeoutId = null

const startRecording = async() => {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true })

    recorder = new RecordRTC(micStream, {
        type: "audio",
        mimeType: "audio/wav",
        recorderType: StereoAudioRecorder,
        desiredSampleRate: 44100,
        numberOfAudioChannels: 1
    })

    recorder.startRecording()
    isRecording = true
    rxRecordBtn.textContent = "Stop"
    rxRecordBtn.classList.add("border-red", "text-red")
    rxRecordStatus.classList.remove("hidden")
    rxRecordStatus.textContent = "recording... (auto-stops at 20s for now)"

    recordTimeoutId = setTimeout(() => stopRecording(), MAX_RECORD_MS)
}

const stopRecording = () => {
    clearTimeout(recordTimeoutId)
    if(!recorder || !isRecording) return

    recorder.stopRecording(() => {
        const wavBlob = recorder.getBlob()
        micStream.getTracks().forEach(t => t.stop())
        pendingBlob = wavBlob
        rxRecordStatus.textContent = "recorded, ready to decode"
    })

    isRecording = false
    rxRecordBtn.textContent = "Record"
    rxRecordBtn.classList.remove("border-red", "text-red")
}


rxRecordBtn.addEventListener("click", async() => {
    if(isRecording) {
        console.log("eee")
        stopRecording()
        return
    }

    try {
        rxRecordStatus.classList.remove("hidden")
        await startRecording()
    } catch(e) {
        rxRecordStatus.textContent = "mic access failed: " + e.message
    }
})