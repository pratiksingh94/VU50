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



rxBtn.addEventListener('click', async() => {
    const file = rxFile.files[0]
    if(!file) {
        alert("no waveform audio is provided :(")
        return
    }

    rxBtn.disabled = true
    rxReadout.className = "font-mono text-sm bg-bg border border-borderLight rounded p-3 min-h-[44px] whitespace-pre-wrap break-words text-textDim"
    rxReadout.textContent = "decoding..."

    const formData = new FormData()
    formData.append("audio", file)

    try {
        const res = await fetch("/decode", {
            method: "POST",
            body: formData
        })
        const data = await res.json()

        if(!res.ok) throw new Error(data.error || "decode failed");

        rxReadout.className = "font-mono text-sm bg-bg border border-borderLight rounded p-3 min-h-[44px] whitespace-pre-wrap break-words text-green"
        rxReadout.textContent = data.text
    } catch (error) {
        rxReadout.className = "font-mono text-sm bg-bg border border-borderLight rounded p-3 min-h-[44px] whitespace-pre-wrap break-words text-red"
        rxReadout.textContent = error.message
    } finally {
        rxBtn.disabled = false
    }
})