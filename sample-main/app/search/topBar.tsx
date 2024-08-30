import React from 'react';
import styles from '../style.module.css';
import topStyles from '/app/search/style/topstyle.module.css';

interface TopBarProps {
  onSearchClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  onHomeClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

export default function TopBar({ onSearchClick, onHomeClick }: TopBarProps) {
  return (
    <div className={topStyles.topBar}>
    <img src="/image/unimelb.png" alt="Your Image" className={styles.topLeftImage} />
    <div
      style={{
        position: 'fixed',
        top: '50px',
        right: '560px',
        padding: '10px 20px',
        borderRadius: '50px',
        backgroundColor: 'transparent',
        fontFamily: 'Georgia, serif',
        border: 'none',
        fontSize: '20px',
        color: 'white',
        zIndex: 1000,
      }}>
      The University of Melbourne's official source of course and subject information
    </div>
    <button
      onClick={onHomeClick}
      style={{
        position: 'fixed',
        top: '53px',
        right: '480px',
        padding: '10px 20px',
        borderRadius: '50px',
        backgroundColor: 'transparent',
        fontFamily: 'Georgia, serif',
        border: 'none',
        fontSize: '15px',
        cursor: 'pointer',
        color: 'white',
        zIndex: 1000,
      }}
    >
      🏠
    </button>
    <button
      onClick={onHomeClick}
      style={{
        position: 'fixed',
        top: '50px',
        right: '370px',
        padding: '10px 20px',
        borderRadius: '50px',
        backgroundColor: 'transparent',
        fontFamily: 'Georgia, serif',
        border: 'none',
        fontSize: '24px',
        cursor: 'pointer',
        color: 'white',
        zIndex: 1000,
      }}
    >
      Handbook
    </button>
    <div
      style={{
        position: 'fixed',
        top: '60px',
        right: '362px',
        backgroundColor: 'transparent',
        fontFamily: 'Georgia, serif',
        border: 'none',
        fontSize: '20px',
        zIndex: 1000,
      }}
    >
      ➔
    </div>
    <button
      style={{
        position: 'fixed',
        top: '50px',
        right: '263px',
        padding: '10px 20px',
        borderRadius: '50px',
        backgroundColor: 'transparent',
        fontFamily: 'Georgia, serif',
        border: 'none',
        fontSize: '24px',
        cursor: 'pointer',
        color: 'white',
        zIndex: 1000,
      }}
    >
      Search
    </button>
    <button
      onClick={onSearchClick}  
      style={{
        position: 'fixed',
        top: '30px',
        right: '70px',
        backgroundColor: 'transparent',
        border: 'none',
        cursor: 'pointer',
        zIndex: 1001,
      }}
    >
      <img src="/image/search.png" alt="Button Image" style={{ width: '80px', height: '75px' }} />
    </button>
  </div>
  );
}
