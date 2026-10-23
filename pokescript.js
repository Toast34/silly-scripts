let running = true;

async function press(key) {
    const target = document.activeElement || document.body;

    target.dispatchEvent(new KeyboardEvent("keydown", {
        key: key,
        code: key === " " ? "Space" : "Digit1",
        keyCode: key === " " ? 32 : 49,
        which: key === " " ? 32 : 49,
        bubbles: true,
        cancelable: true
    }));

    await new Promise(r => setTimeout(r, 100));

    target.dispatchEvent(new KeyboardEvent("keyup", {
        key: key,
        code: key === " " ? "Space" : "Digit1",
        keyCode: key === " " ? 32 : 49,
        which: key === " " ? 32 : 49,
        bubbles: true,
        cancelable: true
    }));
}

async function loop() {
    while (running) {
        await press("1");
        await press(" ");
        await press("1");
        await new Promise(r => setTimeout(r, 10));
    }
}

loop();