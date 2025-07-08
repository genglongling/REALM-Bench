import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        transform: string;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export type ArrowProps = typeof __propDef.props;
export type ArrowEvents = typeof __propDef.events;
export type ArrowSlots = typeof __propDef.slots;
export default class Arrow extends SvelteComponent<ArrowProps, ArrowEvents, ArrowSlots> {
}
export {};
