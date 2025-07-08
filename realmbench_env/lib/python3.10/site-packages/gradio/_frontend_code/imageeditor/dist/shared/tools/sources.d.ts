import { type Container, type IRenderer, type ColorSource } from "pixi.js";
import { type Command } from "../utils/commands";
interface BgImageCommand extends Command {
    /**
     * Initial setup for the bg command
     * @returns
     */
    start: () => Promise<[number, number]>;
}
/**
 * Adds a background image to the canvas.
 * @param container The container to add the image to.
 * @param renderer The renderer to use for the image.
 * @param background The background image to add.
 * @param resize The function to resize the canvas.
 * @returns A command that can be used to undo the action.
 */
export declare function add_bg_image(container: Container, renderer: IRenderer, background: Blob | File, resize: (width: number, height: number) => void, max_height?: number): BgImageCommand;
/**
 * Command that sets a background
 */
interface BgColorCommand extends Command {
    /**
     * Initial setup for the bg command
     * @returns
     */
    start: () => [number, number];
}
/**
 * Adds a background color to the canvas.
 * @param container The container to add the image to.
 * @param renderer The renderer to use for the image.
 * @param color The background color to add.
 * @param width The width of the background.
 * @param height The height of the background.
 * @param resize The function to resize the canvas.
 * @returns A command that can be used to undo the action.
 */
export declare function add_bg_color(container: Container, renderer: IRenderer, color: ColorSource, width: number, height: number, resize: (width: number, height: number) => void): BgColorCommand;
export {};
