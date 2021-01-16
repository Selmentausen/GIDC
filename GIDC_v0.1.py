from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from calculate_damage import get_damage_calculations
import sys


class GIDC(QMainWindow):
    def __init__(self):
        super(GIDC, self).__init__()
        uic.loadUi('mainWindow.ui', self)
        self.setWindowTitle('GIDC')
        self.calculateButton.clicked.connect(self.calculate_dmg)
        self.data = {}

    def check_talent_multiplier_input(self, text) -> bool:
        return not all(map(lambda x: x.strip().isdigit(), text.split(';')))

    def get_data(self):
        try:
            self.data['char_atk'] = int(self.atkEdit.text())
            self.data['elem_bonus'] = float(self.elemEdit.text().replace(',', '.'))
            self.data['special_bonus'] = float(self.specialEdit.text().replace(',', '.'))
            self.data['talent_multi'] = self.talentEdit.text().replace(',', '.')
            if self.check_talent_multiplier_input(self.data['talent_multi']):
                raise ValueError
            self.data['char_lvl'] = int(self.characterLevelEdit.text())
            self.data['crit_rate'] = float(self.critRateEdit.text().replace(',', '.'))
            self.data['crit_dmg'] = float(self.critDamageEdit.text().replace(',', '.'))
            self.data['attack_count'] = int(self.attackCountEdit.text())
            self.data['enemy_lvl'] = int(self.enemyLevelEdit.text())
            self.data['enemy_elem_res'] = int(self.enemyElemResEdit.text())
            self.data['enemy_phys_res'] = int(self.enemyPhysResEdit.text())
            self.data['dmg_type'] = self.damageTypeBox.currentText()
            return True
        except ValueError:
            self.statusBar().showMessage('Incorrect input data')
            return False
        except BaseException as err:
            self.statusBar().showMessage(str(err))
            return False

    def calculate_dmg(self):
        # Get user input data
        if self.get_data():
            single_hit, single_crit, total_dmg = get_damage_calculations(self.data)

            self.sadLabel.setText(f'Single Attack Damage: {single_hit}')
            self.scdLabel.setText(f'Single Crit Damage: {single_crit}')
            self.tadLabel.setText(f'Total Attack Damage: {total_dmg}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gidc = GIDC()
    gidc.show()
    sys.exit(app.exec())
