import json
import logging
from datetime import datetime
from typing import Any

from playwright.sync_api import sync_playwright, Page


def track_interaction(interactions: list[dict[str, Any]], interaction_type: str, details: dict[str, Any]):
    interactions.append({
        "type": interaction_type,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })
    logging.debug(f"Tracked interaction: {interaction_type}")


def make_handler(interactions: list[dict[str, Any]]):
    def handle_interaction(interaction_type: str, details_json: str):
        track_interaction(interactions, interaction_type, json.loads(details_json))

    return handle_interaction


def inject_user_interaction_tracking(page: Page, interactions: list):
    js_code = """
    function sendInteraction(type, details) {
        window.registerInteraction(type, JSON.stringify(details));
    }

    const interactionProperties = {
        'click': 'button',
        'dblclick': 'button',
        'mousedown': 'button',
        'mouseup': 'button',
        'keydown': 'key',
        'keyup': 'key',
        'input': 'value',
        'change': 'value',
        'scroll': () => ({ x: window.scrollX, y: window.scrollY }),
        'dragstart': null,
        'dragend': null,
        'drop': null,
        'focus': null,
        'blur': null
    };

    function getInteractionDetails(event, property) {
        if (property === null) {
            return {};
        }
        if (typeof property === 'function') {
            return property(event);
        }
        return { [property]: event[property] };
    }

    Object.entries(interactionProperties).forEach(([event, property]) => {
        document.addEventListener(event, (e) => {
            const details = getInteractionDetails(e, property);
            details.target = e.target.outerHTML;
            sendInteraction(event, details);
        }, ['focus', 'blur'].includes(event));
    });

    document.addEventListener('change', (e) => {
        if (e.target.tagName.toLowerCase() === 'select') {
            sendInteraction('select', {
                options: Array.from(e.target.selectedOptions).map(option => option.value),
                target: e.target.outerHTML
            });
        }
    });
    console.log('Event listeners set up');
    """

    page.expose_function("registerInteraction", make_handler(interactions))
    page.add_init_script(js_code)


def track_interactions_to_file(start_url: str, output_file: str, headless: bool):
    interactions = []

    logging.info(f"Starting browser, headless={headless}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        inject_user_interaction_tracking(page, interactions)
        logging.info(f"Navigating to {start_url}")
        page.goto(start_url)

        print("Tracking user interactions. Close the browser to stop.")

        try:
            page.wait_for_event('close', timeout=0)
        except KeyboardInterrupt:
            pass

    logging.info(f"Saving interactions to {output_file}")
    with open(output_file, 'w') as f:
        json.dump({"interactions": interactions}, f, indent=2)
