import { SvelteComponent } from "svelte";
export { default as BaseDataFrame } from "./shared/Table.svelte";
export { default as BaseExample } from "./Example.svelte";
import type { Gradio, SelectData } from "@gradio/utils";
import type { LoadingStatus } from "@gradio/statustracker";
import type { Headers, Data, Metadata, Datatype } from "./shared/utils";
declare const __propDef: {
    props: {
        headers?: Headers | undefined;
        elem_id?: string | undefined;
        elem_classes?: string[] | undefined;
        visible?: boolean | undefined;
        value?: {
            data: Data;
            headers: Headers;
            metadata: Metadata;
        } | undefined;
        value_is_output?: boolean | undefined;
        col_count: [number, "fixed" | "dynamic"];
        row_count: [number, "fixed" | "dynamic"];
        label?: (string | null) | undefined;
        show_label?: boolean | undefined;
        wrap: boolean;
        datatype: Datatype | Datatype[];
        scale?: (number | null) | undefined;
        min_width?: number | undefined;
        root: string;
        line_breaks?: boolean | undefined;
        column_widths?: string[] | undefined;
        gradio: Gradio<{
            change: never;
            select: SelectData;
            input: never;
            clear_status: LoadingStatus;
        }>;
        latex_delimiters: {
            left: string;
            right: string;
            display: boolean;
        }[];
        max_height?: number | undefined;
        loading_status: LoadingStatus;
        interactive: boolean;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export type IndexProps = typeof __propDef.props;
export type IndexEvents = typeof __propDef.events;
export type IndexSlots = typeof __propDef.slots;
export default class Index extends SvelteComponent<IndexProps, IndexEvents, IndexSlots> {
}
