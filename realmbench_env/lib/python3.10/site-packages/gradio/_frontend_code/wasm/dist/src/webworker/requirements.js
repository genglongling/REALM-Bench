export function verifyRequirements(requirements) {
    requirements.forEach((req) => {
        let url;
        try {
            url = new URL(req);
        }
        catch {
            // `req` is not a URL -> OK
            return;
        }
        // Ref: The scheme checker in the micropip implementation is https://github.com/pyodide/micropip/blob/v0.1.0/micropip/_compat_in_pyodide.py#L23-L26
        if (url.protocol === "emfs:" || url.protocol === "file:") {
            throw new Error(`"emfs:" and "file:" protocols are not allowed for the requirement (${req})`);
        }
    });
}
