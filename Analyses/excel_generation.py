import io
import pandas as pd

def generate_excel_report(result_df, start_date, end_date):
    # Créer un objet BytesIO pour stocker les données Excel
    output = io.BytesIO()

    # Multipliez par 100 pour obtenir la représentation en pourcentage correcte
    result_df['%'] /= 100

    # Utiliser Pandas pour sauvegarder le DataFrame au format Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='Bilan de la période', startrow=2, index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Bilan de la période']

        # Mise en page pour l'impression
        worksheet.set_paper(9)  # Papier A4
        worksheet.center_horizontally()
        worksheet.fit_to_pages(1, 1)

        # Pied de page
        worksheet.set_footer('&L&D &T&CPage &P sur &N')

        # Supprimer l'affichage du quadrillage
        worksheet.hide_gridlines(2)

        # Définit le zoom à 130%
        worksheet.set_zoom(130)

        # Créer un format personnalisé pour les en-têtes de colonnes
        header_format = writer.book.add_format({
            'bold': True,
            'text_wrap': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'red',
            'font_color': 'white',
            'border': 1,
            'font_size': 12
        })

        # Appliquer le format aux en-têtes de colonnes
        for col_num, value in enumerate(result_df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Formatage des cellules pour les 4 premières lignes de chaque colonne
        custom_format = writer.book.add_format({
            'font_size': 11,
            'bold': True,
            'border': 1,
            'fg_color': '#E2E2E2'
        })

        formats = {
            'A': custom_format,
            'B': writer.book.add_format({'num_format': '#,##0', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'}),
            'C': writer.book.add_format({'num_format': '0.00%', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'}),
            'D': writer.book.add_format({'num_format': '#,##0.00 €', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'}),
            'E': writer.book.add_format({'num_format': '#,##0.00 €', 'font_size': 11, 'border': 1, 'fg_color': '#E2E2E2'})
        }

        for row in range(1, len(result_df) + 1):
            for col, col_format in formats.items():
                worksheet.write(row, ord(col) - 65, result_df.iat[row-1, ord(col) - 65], col_format)

        # Définition de la largeur pour chaque colonne
        worksheet.set_column('A:A', len('Type') + 4)
        worksheet.set_column('B:B', len('Nbr Couverts') + 2)
        worksheet.set_column('C:C', len('%') + 10)
        worksheet.set_column('D:D', len('Total Additions €') + 2)
        worksheet.set_column('E:E', len('Panier moyen €') + 2)

    # Définir le point de départ pour la lecture
    output.seek(0)

    return output
