import type { SetupParser } from "./types";
import { IracingStoParser } from "./iracing/sto-parser";

/**
 * Parser registry — resolves the right parser for a given filename.
 * New parsers are registered here.
 */
export class ParserRegistry {
  private parsers: SetupParser[] = [];

  constructor() {
    // Register built-in parsers
    this.register(new IracingStoParser());
  }

  register(parser: SetupParser): void {
    this.parsers.push(parser);
  }

  /** Find a parser that supports the given filename */
  findParser(filename: string): SetupParser | null {
    return this.parsers.find((p) => p.supports(filename)) ?? null;
  }

  /** Get all registered parsers */
  getAll(): readonly SetupParser[] {
    return this.parsers;
  }

  /** Get all supported file extensions */
  getSupportedExtensions(): string[] {
    return this.parsers.flatMap((p) => p.supportedExtensions);
  }
}

/** Singleton instance */
export const parserRegistry = new ParserRegistry();
