from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class GIDC(QMainWindow):
    def __init__(self):
        super(GIDC, self).__init__()
        uic.loadUi('mainWindow.ui', self)
        self.calculateButton.clicked.connect(self.calculate_dmg)

    def get_data(self):
        try:
            self.char_atk = int(self.atkEdit.text())
            self.elem_bonus = float(self.elemEdit.text())
            self.special_bonus = float(self.specialEdit.text())
            self.talent_multi = float(self.talentEdit.text())
            self.char_lvl = int(self.characterLevelEdit.text())
            self.crit_rate = float(self.critRateEdit.text())
            self.crit_dmg = float(self.critDamageEdit.text())
            self.attack_count = int(self.attackCountEdit.text())
            self.enemy_lvl = int(self.enemyLevelEdit.text())
            self.enemy_elem_res = int(self.enemyElemResEdit.text())
            self.enemy_phys_res = int(self.enemyPhysResEdit.text())
            self.dmg_type = self.damageTypeBox.currentText()
            return True
        except ValueError:
            self.statusBar().showMessage('Incorrect input data')
            return False
        except BaseException as err:
            self.statusBar().showMessage(str(err))
            return False

    def def_dmg_reduction(self):
        defense = 5 * self.enemy_lvl + 500
        return 1 - defense / (defense + 5 * self.char_lvl + 500)

    def res_dmg_reduction(self):
        base_res = self.enemy_elem_res if self.dmg_type == 'Res' else self.enemy_phys_res
        return 1 - base_res / 100

    def calculate_dmg(self):
        # Get user input data
        if self.get_data():

            # Calculate single hit damage and single crit damage
            res_dmg_reduction = self.res_dmg_reduction()
            def_dmg_reduction = self.def_dmg_reduction()
            dmg = int(self.char_atk * (self.talent_multi / 100) * (1 + ((self.special_bonus + self.elem_bonus) / 100)))
            single_hit = int(dmg * def_dmg_reduction * res_dmg_reduction)
            single_crit = int(single_hit * (1 + self.crit_dmg / 100))

            # Display single hit damage
            self.sadLabel.setText(f'Single Attack Damage: {single_hit}')

            # Display single crit damage
            self.scdLabel.setText(f'Single Crit Damage: {single_crit}')

            # Calculate and display total damage
            crit_hits = int(self.attack_count * (self.crit_rate / 100))
            total_crit_dmg = int(single_crit * crit_hits)
            total_dmg = int(total_crit_dmg + (single_hit * (self.attack_count - crit_hits)))
            self.tadLabel.setText(f'Total Attack Damage: {total_dmg}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gidc = GIDC()
    gidc.show()
    sys.exit(app.exec())
