'use client';
import { useState } from 'react';
import dynamic from 'next/dynamic';

export default function HelpButton() {
  const [showChat, setShowChat] = useState(false);

  const DeepChat = dynamic(() => import('deep-chat-react').then((mod) => mod.DeepChat), {
    ssr: false,
  });

  return (
    <>
      {!showChat && (
        <button
          id="help-button"
          style={{
            position: 'fixed',
            bottom: '20px',
            left: '30px',
            padding: '10px 20px',
            borderRadius: '5px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            cursor: 'pointer',
            zIndex: 1000,
          }}
          onClick={() => setShowChat(true)}
        >
          HELP
        </button>
      )}

      {showChat && (
        <div
          style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            width: '400px',
            height: '500px',
            zIndex: 999,
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
          }}
        >
          <button
            style={{
              position: 'absolute',
              top: '0px',
              right: '20px',
              backgroundColor: 'transparent',
              border: 'none',
              fontSize: '16px',
              cursor: 'pointer',
              zIndex: 1002,
            }}
            onClick={() => setShowChat(false)}
          >
            ✖
          </button>

          <DeepChat
            id="chat-element"
            style={{
              borderRadius: '10px',
              borderColor: '#e4e4e4',
              background:
                'linear-gradient(90deg, rgb(239, 242, 247) 0%, 7.60286%, rgb(237, 240, 249) 15.2057%, 20.7513%, rgb(235, 239, 248) 26.297%, 27.6386%, rgb(235, 239, 248) 28.9803%, 38.2826%, rgb(231, 237, 249) 47.585%, 48.1216%, rgb(230, 236, 250) 48.6583%, 53.1306%, rgb(228, 236, 249) 57.6029%, 61.5385%, rgb(227, 234, 250) 65.4741%, 68.7835%, rgb(222, 234, 250) 72.093%, 75.7603%, rgb(219, 230, 248) 79.4275%, 82.8265%, rgb(216, 229, 248) 86.2254%, 87.8354%, rgb(213, 228, 249) 89.4454%, 91.8605%, rgb(210, 226, 249) 94.2755%, 95.4383%, rgb(209, 225, 248) 96.6011%, 98.3005%, rgb(208, 224, 247) 100%)',
              position: 'fixed',
              bottom: '20px',
              right: '20px',
              width: '400px',
              height: '500px',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
              padding: '10px',
              zIndex: 1001,
            }}
            textInput={{
              styles: {
                container: {
                  borderRadius: '20px',
                  border: 'unset',
                  width: '78%',
                  marginLeft: '8px',
                  boxShadow:
                    '0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)',
                },
                text: { padding: '10px', paddingLeft: '15px', paddingRight: '34px' },
              },
              placeholder: { text: 'Ask me anything...', style: { color: '#606060' } },
            }}
            images={true}
            camera={{ button: { position: 'dropup-menu' } }}
            directConnection={{
              openAI: {
                key: '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',
                chat: { max_tokens: 2000, system_prompt: 'Assist me with anything you can' },
              },
            }}
            speechToText={{
              azure: {
                subscriptionKey: '57cc542a7aa24da29f67f90a02c1339a',
                region: 'australiaeast',
              },
              button: {
                default: {
                  container: {
                    default: {
                      bottom: '1em',
                      right: '0.6em',
                      borderRadius: '20px',
                      width: '1.9em',
                      height: '1.9em',
                    },
                  },
                  svg: { styles: { default: { bottom: '0.35em', left: '0.35em' } } },
                },
                position: 'inside-right',
              },
              commands: {
                stop: 'stop',
                pause: 'pause',
                resume: 'resume',
                removeAllText: 'remove text',
                submit: 'submit',
                commandMode: 'command',
              },
            }}
            messageStyles={{
              default: {
                shared: {
                  bubble: {
                    backgroundColor: 'unset',
                    marginTop: '10px',
                    marginBottom: '10px',
                    boxShadow:
                      '0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)',
                  },
                },
                user: {
                  bubble: {
                    background: 'linear-gradient(130deg, #2870EA 20%, #1B4AEF 77.5%)',
                  },
                },
                ai: { bubble: { background: 'rgba(255,255,255,0.7)' } },
              },
            }}
            errorMessages={{
              overrides: {
                speechToText:
                  'Azure Speech To Text can not be used in this website as you need to set your credentials.',
              },
            }}
            submitButtonStyles={{
              position: 'outside-right',
              submit: {
                container: {
                  default: {
                    bottom: '0.8em',
                    borderRadius: '25px',
                    padding: '6px 5px 4px',
                    backgroundColor: 'unset',
                  },
                  hover: { backgroundColor: '#b0deff4f' },
                  click: { backgroundColor: '#b0deffb5' },
                },
                svg: {
                  content:
                    '<?xml version="1.0" encoding="utf-8"?> <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m21.426 11.095-17-8A.999.999 0 0 0 3.03 4.242L4.969 12 3.03 19.758a.998.999 0 0 0 1.396 1.147l17-8a1 1 0 0 0 0-1.81zM5.481 18.197l.839-3.357L12 12 6.32 9.16l-.839-3.357L18.651 12l-13.17 6.197z"/></svg>',
                  styles: {
                    default: {
                      width: '1.5em',
                      filter:
                        'brightness(0) saturate(100%) invert(10%) sepia(86%) saturate(6044%) hue-rotate(205deg) brightness(100%) contrast(100%)',
                    },
                  },
                },
              },
              loading: {
                svg: {
                  styles: {
                    default: {
                      filter:
                        'brightness(0) saturate(100%) invert(72%) sepia(0%) saturate(3044%) hue-rotate(322deg) brightness(100%) contrast(96%)',
                    },
                  },
                },
              },
              stop: {
                container: { hover: { backgroundColor: '#ededed94' } },
                svg: {
                  styles: {
                    default: {
                      filter:
                        'brightness(0) saturate(100%) invert(72%) sepia(0%) saturate(3044%) hue-rotate(322deg) brightness(100%) contrast(96%)',
                    },
                  },
                },
              },
            }}
            demo={true}
            connect={{ stream: true }}
          />
        </div>
      )}
    </>
  );
}
