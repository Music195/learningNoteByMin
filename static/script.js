document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const resultsBox = document.getElementById("search-results");
    const noteSelect = document.getElementById("noteSelect");
    const tagFilter = document.getElementById("tagFilter");

    // Populate tag dropdown
    const tagsSet = new Set();
    Object.values(NOTE_TAGS).forEach(tags => tags.forEach(tag => tagsSet.add(tag)));
    Array.from(tagsSet).sort().forEach(tag => {
        const opt = document.createElement("option");
        opt.value = tag;
        opt.textContent = tag;
        tagFilter.appendChild(opt);
    });

    // Filter notes by tag
    window.filterByTag = () => {
        const selectedTag = tagFilter.value;
        noteSelect.innerHTML = "";
        NOTES_LIST.forEach(note => {
            const tags = NOTE_TAGS[note] || [];
            if (!selectedTag || tags.includes(selectedTag)) {
                const opt = document.createElement("option");
                opt.value = "/note/" + note;
                opt.textContent = note.charAt(0).toUpperCase() + note.slice(1);
                noteSelect.appendChild(opt);
            }
        });
    };

    // Fuzzy search with Fuse.js
    const fuse = new Fuse(NOTES_LIST, { includeScore: true, threshold: 0.4 });

    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim();
        resultsBox.innerHTML = "";
        if (!query) return;
        const results = fuse.search(query).slice(0, 10);
        results.forEach(result => {
            const a = document.createElement("a");
            a.href = "/note/" + result.item;
            a.textContent = result.item;
            resultsBox.appendChild(a);
        });
    });

    // Arrow key navigation
    document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft") {
            const back = document.querySelector(".nav-buttons a:first-child");
            if (back) window.location.href = back.href;
        }
        if (e.key === "ArrowRight") {
            const next = document.querySelector(".nav-buttons a:last-child");
            if (next) window.location.href = next.href;
        }
    });
});