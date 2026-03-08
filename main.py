#!/usr/bin/env python3
"""
NeuroString – Hlavní spouštěcí soubor
"""

import os
import sys
import time
from datetime import datetime
from node import NeuroNode
from network import NeuroNetwork
from neuropilot import NeuroPilot
from web import app
import threading

def print_logo():
    """Vytiskne logo NeuroStringu"""
    logo = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗          ║
    ║   ████╗  ██║██╔════╝██║   ██║██╔══██╗██╔═══██╗         ║
    ║   ██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║   ██║         ║
    ║   ██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║         ║
    ║   ██║ ╚████║███████╗╚██████╔╝██║  ██║╚██████╔╝         ║
    ║   ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝          ║
    ║                                                          ║
    ║   ███████╗████████╗██████╗ ██╗███╗   ██╗ ██████╗        ║
    ║   ██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║██╔════╝        ║
    ║   ███████╗   ██║   ██████╔╝██║██╔██╗ ██║██║  ███╗       ║
    ║   ╚════██║   ██║   ██╔══██╗██║██║╚██╗██║██║   ██║       ║
    ║   ███████║   ██║   ██║  ██║██║██║ ╚████║╚██████╔╝       ║
    ║   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝        ║
    ║                                                          ║
    ║        První decentralizovaná síť, která myslí          ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(logo)
    print(f"\n🔮 Verze: 0.1.0 (Alpha)")
    print(f"📅 Spuštěno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"⚡ Stav: Neuronová síť aktivována\n")

def main():
    """Hlavní funkce"""
    # Vymaž obrazovku
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Zobraz logo
    print_logo()
    
    # Inicializuj síť
    print("🔄 Inicializuji NeuroString síť...")
    network = NeuroNetwork()
    
    # Přidej první uzly
    print("🧠 Vytvářím první neurony...")
    for i in range(3):
        node = NeuroNode(node_id=f"node_{i}")
        network.add_node(node)
        print(f"   ✓ Uzel {node.node_id} vytvořen (synapsí: {len(node.synapses)})")
    
    # Spusť síť
    print("\n⚡ Aktivuji kvantové provázání...")
    network.activate_quantum_entanglement()
    
    # Spusť webové rozhraní v samostatném vlákně
    print("🌐 Spouštím webové rozhraní na portu 5000...")
    web_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False))
    web_thread.daemon = True
    web_thread.start()
    
    # Inicializuj NeuroPilot
    pilot = NeuroPilot(network)

    # Hlavní smyčka
    print("\n📡 Síť běží. Příkazy: [T]ransakce, [S]tav, [I]nfo, [P]ilot, [Q]uit\n")
    
    try:
        while True:
            cmd = input("NeuroString> ").strip().upper()
            
            if cmd == "T":
                # Simuluj transakci
                data = f"transakce_{datetime.now().timestamp()}"
                print(f"📤 Odesílám: {data}")
                result = network.process_transaction(data)
                print(f"📥 Výsledek: {result}")
                
            elif cmd == "S":
                # Zobraz stav sítě
                print("\n" + "="*50)
                print("📊 STAV SÍTĚ")
                print("="*50)
                print(f"Počet uzlů: {len(network.nodes)}")
                print(f"Kvantová provázanost: {network.entanglement_level:.2%}")
                print(f"Celkový počet synapsí: {network.total_synapses()}")
                print(f"Paměťové vzory: {network.memory_patterns}")
                print("="*50 + "\n")
                
            elif cmd == "I":
                # Info o projektu
                print("\n" + "="*50)
                print("ℹ️  O PROJEKTU")
                print("="*50)
                print("NeuroString kombinuje:")
                print("🧠 Neuronové sítě - adaptivní uzly")
                print("⚛️  Kvantovou fyziku - okamžitý konsenzus")
                print("🌌 Teorii strun - 11D úložiště")
                print("="*50 + "\n")

            elif cmd == "P":
                # NeuroPilot – automatický pilot
                if pilot.running:
                    pilot.stop()
                    status = pilot.get_status()
                    print(f"📊 Celkem provedeno akcí: {status['actions']} za {status['elapsed_seconds']} s")
                else:
                    pilot.start()
                    print("💡 Zadej znovu [P] pro zastavení pilota.")
                
            elif cmd == "Q":
                print("\n👋 Ukončuji NeuroString...")
                break
                
            else:
                print("❌ Neznámý příkaz. Zkuste T, S, I, P nebo Q.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Ukončuji NeuroString...")
    finally:
        if pilot.running:
            pilot.stop()
    
    print("✅ Hotovo.")

if __name__ == "__main__":
    main()
