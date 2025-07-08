import { SvelteComponent } from "svelte";
declare const __propDef: {
    props: {
        expanded?: boolean | undefined;
        title: string;
        rtl?: boolean | undefined;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {};
    };
};
export type MessageBoxProps = typeof __propDef.props;
export type MessageBoxEvents = typeof __propDef.events;
export type MessageBoxSlots = typeof __propDef.slots;
export default class MessageBox extends SvelteComponent<MessageBoxProps, MessageBoxEvents, MessageBoxSlots> {
}
export {};
