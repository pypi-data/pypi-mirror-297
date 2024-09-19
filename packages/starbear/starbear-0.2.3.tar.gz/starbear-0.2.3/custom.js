
class Eventotron extends HTMLElement {
    constructor() {
        console.log("BUILD IT!");
        super();
        console.log(this.children);

        this.onMutation = this.onMutation.bind(this);
    }

    connectedCallback() {
        // Set up observer
        this.observer = new MutationObserver(this.onMutation);

        // Watch the Light DOM for child node changes
        this.observer.observe(this, {
            childList: true,
            subtree: true,
        });
    }

    disconnectedCallback() {
        // remove observer if element is no longer connected to DOM
        this.observer.disconnect();
    }

    onMutation(mutations) {
        console.log(mutations);
        // const added = [];

        // // A `mutation` is passed for each new node
        // for (const mutation of mutations) {
        //   // Could test for `mutation.type` here, but since we only have
        //   // set up one observer type it will always be `childList`
        //   added.push(...mutation.addedNodes);
        // }

        // console.log({
        //       // filter out non element nodes (TextNodes etc.)
        //       added: added.filter(el => el.nodeType === Node.ELEMENT_NODE),
        // });
    }
}

window.customElements.define("event-o-tron", Eventotron);
