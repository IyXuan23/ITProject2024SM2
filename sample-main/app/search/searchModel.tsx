import React from 'react';

interface SearchModalProps {
  onClose: () => void;
}

export default function SearchModal({ onClose }: SearchModalProps) {
  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
      }}
    >
      <input
        type="text"
        placeholder="Search the Handbook"
        style={{
          width: '60%',
          padding: '15px',
          fontSize: '24px',
          borderRadius: '5px',
          border: '1px solid #ccc',
        }}
      />
      <button
        style={{
          position: 'absolute',
          top: '20px',
          right: '20px',
          backgroundColor: 'transparent',
          border: 'none',
          fontSize: '24px',
          cursor: 'pointer',
        }}
        onClick={onClose}
      >
        &#10005;
      </button>
    </div>
  );
}
