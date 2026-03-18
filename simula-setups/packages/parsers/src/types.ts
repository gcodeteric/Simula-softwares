/**
 * Setup file parser interface.
 *
 * Strategy pattern: each sim implements this interface.
 * For MVP, the iRacing .sto parser is a stub that stores
 * the raw file but doesn't extract parameters (they come
 * from manual user input).
 */
export interface SetupParser {
  /** Unique identifier for this parser (e.g., "iracing-sto") */
  readonly id: string;

  /** Human-readable name */
  readonly name: string;

  /** Sim this parser handles */
  readonly sim: string;

  /** File extensions this parser supports (e.g., [".sto"]) */
  readonly supportedExtensions: string[];

  /** Check if this parser can handle the given filename */
  supports(filename: string): boolean;

  /** Parse a setup file buffer and extract what we can */
  parse(buffer: Buffer, filename: string): Promise<ParseResult>;
}

export interface ParseResult {
  /** SHA-256 hash of the file */
  fileHash: string;

  /** Extracted parameters (may be empty if format is binary/proprietary) */
  parameters: Record<string, unknown>;

  /** Whether parameters were fully extracted or if manual input is needed */
  parametersComplete: boolean;

  /** Hints about the car (if detectable from the file) */
  carHint?: string;

  /** Hints about the track (if detectable from the file) */
  trackHint?: string;

  /** Any warnings during parsing */
  warnings: string[];
}

/** Setup parameter category for organizing the manual input form */
export type SetupCategory =
  | "tires"
  | "suspension"
  | "chassis"
  | "brakes"
  | "aero"
  | "fuel"
  | "differential"
  | "gearing"
  | "electronics";
