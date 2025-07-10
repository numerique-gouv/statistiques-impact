import { MigrationInterface, QueryRunner } from "typeorm";

export class AddFieldsToIndicator1689600273651 implements MigrationInterface {
    name = 'AddFieldsToIndicator1689600273651'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" ADD "indicateur" character varying NOT NULL`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "valeur" integer NOT NULL`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "unite_mesure" character varying NOT NULL`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "frequence_calcul" character varying NOT NULL`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "date" TIMESTAMP WITH TIME ZONE NOT NULL`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "est_periode" boolean NOT NULL`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "est_periode"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "date"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "frequence_calcul"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "unite_mesure"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "valeur"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "indicateur"`);
    }

}
