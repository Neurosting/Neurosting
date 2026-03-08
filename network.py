#!/usr/bin/env python3
"""
NeuroString – Třída NeuroNetwork (správa sítě)
"""

import random
import threading
import numpy as np
from node import NeuroNode

class NeuroNetwork:
    """Třída pro správu celé NeuroString sítě"""
    
    def __init__(self):
        """Inicializace sítě"""
        self._nodes = {}  # {node_id: NeuroNode}
        self._transaction_history = []
        self._entanglement_level = 0.0
        self._memory_patterns = 0
        self.consensus_threshold = 0.67  # 67% shoda pro konsenzus
        self._lock = threading.RLock()  # RLock pro thread-safe přístup k síti
        
    def add_node(self, node):
        """Přidá uzel do sítě a vytvoří synapse"""
        with self._lock:
            self._nodes[node.node_id] = node
            
            # Vytvoř synapse s existujícími uzly
            for existing_node in self._nodes.values():
                if existing_node.node_id != node.node_id:
                    # Náhodně vytvoř spojení
                    if random.random() > 0.5:
                        node.add_synapse(existing_node.node_id)
                        existing_node.add_synapse(node.node_id)
    
    def add_node_if_below(self, node, max_nodes):
        """Atomicky přidá uzel pokud celkový počet uzlů v síti je pod max_nodes.

        Kontrola a přidání probíhají pod jedním zámkem, takže nehrozí
        situace kdy dvě vlákna obě ověří podmínku a obě ji překročí.

        Returns:
            True pokud byl uzel přidán, False pokud kapacita byla dosažena.
        """
        with self._lock:
            if len(self._nodes) >= max_nodes:
                return False
            self.add_node(node)  # RLock umožňuje opakované zamčení
            return True
    
    def remove_node(self, node_id):
        """Odstraní uzel ze sítě"""
        with self._lock:
            if node_id in self._nodes:
                # Odstraň všechny synapse na tento uzel
                for node in self._nodes.values():
                    if node_id in node.synapses:
                        node.remove_synapse(node_id)
                
                # Smaž uzel
                del self._nodes[node_id]
    
    def activate_quantum_entanglement(self):
        """Aktivuje kvantové provázání mezi uzly"""
        with self._lock:
            if len(self._nodes) < 2:
                self._entanglement_level = 0.0
                return
            
            # Simulace kvantového provázání
            pairs = 0
            total_possible = len(self._nodes) * (len(self._nodes) - 1) / 2
            
            node_list = list(self._nodes.values())
            for i in range(len(node_list)):
                for j in range(i+1, len(node_list)):
                    if random.random() > 0.3:  # 70% šance na provázání
                        pairs += 1
            
            self._entanglement_level = pairs / total_possible if total_possible > 0 else 0
    
    def process_transaction(self, data):
        """Zpracuje transakci v síti"""
        with self._lock:
            if not self._nodes:
                return "❌ Žádné uzly v síti"
            
            # Náhodně vyber počáteční uzel
            start_node = random.choice(list(self._nodes.values()))
            
            # Zpracuj data
            result = start_node.process_data(data)
            
            if result:
                # Propaguj sítí (simulace šíření vzruchu)
                self._propagate_spike(result, start_node.node_id)
                
                # Zaznamenej transakci
                self._transaction_history.append({
                    'data': data,
                    'timestamp': result['timestamp'],
                    'node': start_node.node_id,
                    'vibration': result['vibration']['fingerprint'][:10]
                })
                
                # Aktualizuj počet vzorů
                self._memory_patterns = len(self._transaction_history)
                
                return f"✅ Transakce zpracována | Otisk: {result['vibration']['fingerprint'][:10]}"
            else:
                return "⚠️  Nízký aktivační potenciál – transakce čeká"
    
    def _propagate_spike(self, spike, from_node_id):
        """Propaguje vzruch sítí (simulace šíření).

        Tato metoda musí být volána pouze z kontextu, kde je již držen
        ``self._lock`` (tzn. výhradně z ``process_transaction``).
        """
        # Najdi všechny uzly s přímým spojením na zdroj
        propagated = set([from_node_id])
        to_process = [from_node_id]
        
        while to_process and len(propagated) < len(self._nodes):
            current = to_process.pop(0)
            
            if current in self._nodes:
                node = self._nodes[current]
                
                # Projdi všechny synapse
                for target_id, strength in node.synapses.items():
                    if target_id not in propagated and target_id in self._nodes:
                        # Přenos vzruchu
                        if random.random() < strength:
                            propagated.add(target_id)
                            to_process.append(target_id)
                            
                            # Učení (Hebbian)
                            target_node = self._nodes[target_id]
                            target_node.learn(current, True)
                            node.learn(target_id, True)
    
    def get_consensus(self, data):
        """Získá konsenzus sítě o datech"""
        with self._lock:
            if not self._nodes:
                return None
            
            # Simulace hlasování (kvantově inspirované)
            votes = []
            for node in self._nodes.values():
                # Kvantově pravděpodobnostní hlasování
                probability = node.activation_potential * random.uniform(0.8, 1.2)
                votes.append(probability > 0.5)
            
            agreement = sum(votes) / len(votes)
            
            if agreement >= self.consensus_threshold:
                return True  # Konsenzus dosažen
            else:
                return False  # Konsenzus nedosažen
    
    def total_synapses(self):
        """Vrátí celkový počet synapsí v síti"""
        with self._lock:
            total = 0
            for node in self._nodes.values():
                total += len(node.synapses)
            return total // 2  # Každá synapse se počítá dvakrát
    
    def get_network_state(self):
        """Vrátí stav celé sítě.

        Používá ``RLock`` (reentrantní zámek), protože interně volá
        ``total_synapses()``, která zámek také zamyká.
        """
        with self._lock:
            return {
                'nodes': len(self._nodes),
                'synapses': self.total_synapses(),
                'transactions': len(self._transaction_history),
                'entanglement': self._entanglement_level,
                'memory_patterns': self._memory_patterns
            }
