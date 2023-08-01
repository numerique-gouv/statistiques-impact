import { MigrationInterface, QueryRunner } from "typeorm";

export class AddUniqueConstraintNomService1690882822574 implements MigrationInterface {
    name = 'AddUniqueConstraintNomService1690882822574'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" ADD CONSTRAINT "One unique value for indicator by frequence and date" UNIQUE ("nom_service_public_numerique", "indicateur", "frequence_calcul", "date")`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" DROP CONSTRAINT "One unique value for indicator by frequence and date"`);
    }

}
