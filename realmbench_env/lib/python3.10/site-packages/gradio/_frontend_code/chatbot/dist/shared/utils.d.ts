import type { FileData } from "@gradio/client";
import type { ComponentType, SvelteComponent } from "svelte";
import type { TupleFormat, ComponentMessage, ComponentData, NormalisedMessage, Message } from "../types";
import { Gradio } from "@gradio/utils";
export declare const format_chat_for_sharing: (chat: NormalisedMessage[]) => Promise<string>;
export interface UndoRetryData {
    index: number | [number, number];
    value: string | FileData | ComponentData;
}
export interface EditData {
    index: number | [number, number];
    value: string;
}
export declare function normalise_messages(messages: Message[] | null, root: string): NormalisedMessage[] | null;
export declare function normalise_tuples(messages: TupleFormat, root: string): NormalisedMessage[] | null;
export declare function is_component_message(message: NormalisedMessage): message is ComponentMessage;
export declare function is_last_bot_message(messages: NormalisedMessage[], all_messages: NormalisedMessage[]): boolean;
export declare function group_messages(messages: NormalisedMessage[], msg_format: "messages" | "tuples"): NormalisedMessage[][];
export declare function load_components(component_names: string[], _components: Record<string, ComponentType<SvelteComponent>>, load_component: Gradio["load_component"]): Promise<Record<string, ComponentType<SvelteComponent>>>;
export declare function get_components_from_messages(messages: NormalisedMessage[] | null): string[];
