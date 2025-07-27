// components/ui/dropzone.tsx

import { useDropzone, DropzoneOptions, FileWithPath } from "react-dropzone";

interface DropzoneProps extends DropzoneOptions {
  /**
   * Called when files are dropped or selected.
   */
  onDrop: (acceptedFiles: FileWithPath[], fileRejections: import("react-dropzone").FileRejection[]) => void;
}

export function Dropzone({ onDrop, ...props }: DropzoneProps) {
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    acceptedFiles,
    fileRejections,
  } = useDropzone({ onDrop, ...props });

  return (
    <div {...getRootProps()} className="your-dropzone-styles">
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop files here ...</p>
      ) : (
        <p>Drag & drop some files, or click to select files</p>
      )}
      <ul>
        {acceptedFiles.map((f) => (
          <li key={f.path ?? f.name}>{f.path ?? f.name}</li>
        ))}
      </ul>
      {/* Show rejections if you want */}
      {fileRejections.length > 0 && (
        <ul>
          {fileRejections.map((rej, idx) => (
            <li key={idx} style={{ color: "red" }}>
              {rej.file.name}: {rej.errors.map(e => e.message).join(", ")}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
